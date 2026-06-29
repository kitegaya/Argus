.PHONY: up cluster observability jenkins infra demo down logs

CLUSTER_NAME=argus

up: cluster observability jenkins
	@echo "Argus local environment is up. Jenkins at http://localhost:8080"

cluster:
	kind create cluster --name $(CLUSTER_NAME) || true
	kubectl apply -f app/k8s-manifests/

observability:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo add grafana https://grafana.github.io/helm-charts || true
	helm repo update
	helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
		-f observability/prometheus-values.yaml -n monitoring --create-namespace
	kubectl apply -f observability/alert-rules.yaml -n monitoring

jenkins:
	docker compose -f jenkins/jenkins-docker-compose.yml up -d

infra:
	cd infra && terraform init && terraform apply -auto-approve

demo:
	ansible-playbook chaos/inject-pod-kill.yml

down:
	docker compose -f jenkins/jenkins-docker-compose.yml down
	kind delete cluster --name $(CLUSTER_NAME)

logs:
	docker logs -f jenkins
