# Argus — AI-Assisted Incident Response

A complete incident response system built with Kubernetes, Prometheus, Jenkins, Ansible, and AI (Groq).

## Architecture

```
Prometheus Rules → Alertmanager → Jenkins Webhook (HTTP POST)
                                          │
                         ┌────────────────▼───────────────────────┐
                         │            Jenkins Pipeline             │
                         │  1. Detect   — log alert payload        │
                         │  2. Classify — rules + Groq AI enrich   │
                         │  3. Approval — gate for unknown types   │
                         │  4. Remediate— Ansible playbook         │
                         │  5. Document — AI postmortem (Groq)     │
                         │  6. Store    — DynamoDB + S3            │
                         │  7. Notify   — Slack                    │
                         └────────────────────────────────────────┘
                                          │
                               Flask Dashboard (port 5000)
```

## Team Structure

| Track | Responsibility |
|-------|---------------|
| **Track A** | Infrastructure & Detection — Kubernetes, Prometheus, Terraform |
| **Track B** | Orchestration — Jenkins, Ansible, Rules Engine |
| **Track C** | AI & Reporting — Groq, Slack, Dashboard, AWS Storage |

## Quick Start

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y docker.io kubectl ansible git python3 python3-pip

# Python packages
pip3 install openai boto3 requests flask jsonschema

# Ansible Kubernetes collection
ansible-galaxy collection install kubernetes.core
```

### Bring up the full stack

```bash
make up        # KIND cluster + Prometheus stack + Jenkins
make infra     # Terraform → AWS (DynamoDB, S3, SNS)
```

### After `terraform apply`, register credentials in Jenkins

Jenkins → Manage Jenkins → Credentials → Global:

| Credential ID           | Kind        | Value                                |
|-------------------------|-------------|--------------------------------------|
| `argus-dynamodb-table`  | Secret text | output of `terraform output dynamodb_table_name` |
| `argus-s3-bucket`       | Secret text | output of `terraform output s3_bucket_name`      |
| `groq-api-key`          | Secret text | your Groq API key                    |
| `slack-webhook-url`     | Secret text | your Slack incoming webhook URL      |

### Manual webhook test

```bash
python3 scripts/test_jenkins_webhook.py
# or target a different URL:
python3 scripts/test_jenkins_webhook.py --url http://localhost:8080/generic-webhook-trigger/invoke?token=argus-token
```

### Contract validation

```bash
python3 scripts/validate_contract.py classification classification.json
python3 scripts/validate_contract.py postmortem    postmortem.json
```

## Environment Variables

| Variable            | Used by                       | Default               | Description                          |
|---------------------|-------------------------------|-----------------------|--------------------------------------|
| `DYNAMODB_TABLE`    | Jenkinsfile, store_incident, dashboard | `argus-incidents` | DynamoDB table name              |
| `S3_BUCKET`         | Jenkinsfile, store_incident   | `argus-reports-default` | S3 bucket for incident reports     |
| `GROQ_API_KEY`      | ai_enrich, generate_postmortem | *(none)*             | Groq API key; AI gracefully skipped if unset |
| `SLACK_WEBHOOK_URL` | notify_slack                  | *(none)*              | Slack incoming webhook URL; skipped if unset |
| `AWS_DEFAULT_REGION`| Jenkinsfile                   | `us-east-1`           | AWS region                           |

## CI

GitHub Actions (`.github/workflows/ci.yml`) validates on every push/PR:

1. Alertmanager config structure
2. Prometheus rule names and API version
3. `PLAYBOOK_MAP` ↔ `ansible/playbooks/` consistency (Contract Rule 5)
4. Contract schema on `sample_classification.json`
5. Syntax-compile all Python scripts
6. README readability

## Playbook → Alert Mapping

| Alert             | Ansible Playbook         | Action                       |
|-------------------|--------------------------|------------------------------|
| `PodCrashLooping` | `restart-deployment.yml` | Rolling restart               |
| `HighMemoryUsage` | `rollback-deployment.yml`| `kubectl rollout undo`        |
| `HighCPU`         | `scale-up.yml`           | Scale +1 replica              |

## Makefile Commands

```
make up           # Full local stack (KIND + observability + Jenkins)
make cluster      # KIND cluster + deploy app manifests
make observability# Prometheus/Grafana/Alertmanager via Helm
make jenkins      # Start Jenkins via Docker Compose
make infra        # Terraform apply (AWS resources)
make down         # Stop Jenkins + delete KIND cluster
make logs         # Follow Jenkins container logs
```

## Troubleshooting

### Jenkins can't reach Kubernetes

Mount your kubeconfig in the Jenkins container (already in `docker-compose.yml`):
```yaml
volumes:
  - ~/.kube:/root/.kube:ro
```

### Alertmanager not routing to Jenkins

The KIND Docker bridge IP (`172.20.0.1`) is hardcoded in `observability/alertmanager-config.yaml`
and `observability/prometheus-values.yaml`. If it differs on your machine, run:
```bash
docker network inspect kind | grep Gateway
```
and update the two files accordingly.

### Groq AI enrichment silently skipped

Set `GROQ_API_KEY` in the Jenkins credentials store. If unset, classification still
succeeds — only the `likely_cause` field is omitted.

### DynamoDB / S3 errors in `store_incident.py`

Ensure AWS credentials are available inside Jenkins:
```yaml
volumes:
  - ~/.aws:/root/.aws:ro
```
Or use IAM roles if running on EC2.
