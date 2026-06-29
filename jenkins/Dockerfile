FROM jenkins/jenkins:lts

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ansible \
    jq \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --ignore-installed --break-system-packages \
    openai \
    boto3 \
    requests \
    oauthlib \
    requests-oauthlib

# Install kubernetes (without dependencies to avoid conflicts)
RUN pip3 install --ignore-installed --break-system-packages kubernetes --no-deps

# Install Ansible Kubernetes collection
RUN ansible-galaxy collection install kubernetes.core

USER jenkins
