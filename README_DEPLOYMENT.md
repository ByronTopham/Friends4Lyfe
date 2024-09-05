
# Flask Application Deployment
## Overview
This repository demonstrates how to deploy a Flask web application using Docker, Jenkins CI/CD pipeline, and a Kubernetes cluster. Kubernetes is an open-source platform for automating the deployment, scaling, and management of containerized applications. Kubernetes clusters ensure that applications are highly available and can scale as demand increases.

## Table of Contents
- [Dockerfile](#dockerfile)
- [Jenkinsfile](#jenkinsfile)
- [deployment.yaml](#deploymentyaml)
- [network-policy.yaml](#network-policyyaml)
## Prerequisites
Before deploying the application, ensure that you have the following:

- **Kubernetes cluster** (local or cloud-based like GKE, AKS, EKS)
- **kubectl** CLI installed and configured to interact with your Kubernetes cluster
- **Containerized application** image pushed to a container registry (like DockerHub, GCR, or ECR)
- A valid `deployment.yaml` file configured for your application
## Dockerfile
The Flask app is containerized using Docker, ensuring consistent environments across development, testing, and production. The `Dockerfile` defines the environment, including the base image, dependencies, and Flask application code.
- **Benefits of Docker**:
  - Isolation of applications and their dependencies.
  - Portability across environments.
  - Simplified testing and deployment process.


To build a Docker image of the Flask app:
  ```bash
  docker build -t <your-image-name> .
  ```
To run the Docker container:
  ```bash
  docker run -p 5000:5000 <your-image-name>
  ```
## Jenkinsfile
The `Jenkinsfile` automates the CI/CD pipeline for building, testing, and deploying the application. It defines the stages Jenkins will run in sequence.

- **Key Stages**:
  - **Checkout Code:** Fetches the latest version of the code from the source repository.
  - **Build Docker Image:** This stage builds the Docker image from the Dockerfile.
  - **Run Tests:** Runs unit tests or other checks (e.g., using `pytest`, `npm test`, etc.).
  - **Push Docker Image:** Builds the Docker image and pushes it to the specified container registry.
  - **Deploy:** Deploys it to a Kubernetes cluster based on `deployment.yaml` and `network-policy.yaml`.
## deployment.yaml
The `deployment.yaml` is a Kubernetes resource definition file that describes the application deployment, including how many replicas of the application to run and which Docker image to use.
- **Key Sections**
  - **apiVersion:** Kubernetes API version (e.g., apps/v1).
  - **kind:** Resource type (Deployment).
  - **metadata:** Metadata such as the name and labels.
  - **spec:**
    - **replicas:** Number of replicas (e.g., replicas: 3).
    - **template:**
      - **containers:**  Defines the container image and its properties (e.g., ports, environment variables).

To apply the `deployment.yaml` and deploy the application:
```bash
  kubectl apply -f deployment.yaml
```

## network-policy.yaml
The `network-policy.yaml` defines the network rules for controlling the communication between pods and services in the Kubernetes cluster.

- **Key Sections**
  - **apiVersion:** Kubernetes API version (networking.k8s.io/v1).
  - **kind:** Resource type (NetworkPolicy).
  - **metadata:** Metadata such as name and labels.
  - **spec:**
    - **podSelector:** Specifies the pods this network policy applies to.
    - **policyTypes:** Defines whether this is an ingress or egress policy.
    - **ingress/egress:** Defines the allowed traffic rules, such as allowed ports and IP ranges.
To enforce the network policy, apply the `network-policy.yaml`:
```bash
  kubectl apply -f network-policy.yaml
```
## Conclusion
This automated pipeline helps streamline the software development lifecycle, reducing human intervention and increasing the speed and reliability of releases. For more details, please refer to `Flask App - Jenkins CI-CD & K8s Deployment Guide.pdf`.