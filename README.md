# Argus - AI-Assisted Incident Response

A complete incident response system built with Kubernetes, Prometheus, Jenkins, Ansible, and AI.

## Team Structure

- **Track A**: Infrastructure & Detection (Kubernetes, Prometheus, Terraform)
- **Track B**: Orchestration (Jenkins, Ansible, Rules Engine)
- **Track C**: AI & Reporting (Groq, Slack, Dashboard, AWS Storage)

## Getting Started

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y docker.io kubectl ansible git python3 python3-pip

# Python packages
pip3 install openai boto3 requests jsonschema

# Ansible Kubernetes collection
ansible-galaxy collection install kubernetes.core
