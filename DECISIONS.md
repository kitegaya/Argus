# Argus Technical Decisions

## Infrastructure
- **Kubernetes**: KIND (not Minikube) for better networking and faster startup
- **Container runtime**: Docker

## CI/CD
- **Orchestration**: Jenkins running in Docker
- **Pipeline**: Declarative Jenkinsfile in repository

## Monitoring
- **Metrics**: Prometheus with kube-prometheus-stack
- **Alerting**: Alertmanager with webhook to Jenkins

## Cloud (AWS - Free Tier)
- **Database**: DynamoDB
- **Storage**: S3
- **Notifications**: SNS

## AI
- **Provider**: Groq (llama-3.3-70b-versatile)
- **Fallback**: Hardcoded templates when API is unavailable
