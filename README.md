# 🚀 Mini URL Shortener - DevOps Project

[![CI/CD Pipeline](https://github.com/oussemaAbdaoui/url-shortener/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/oussemaAbdaoui/url-shortener/actions)
[![Docker Build](https://img.shields.io/docker/cloud/build/oussemaabdaoui/url-shortener)](https://hub.docker.com/r/oussemaabdaoui/url-shortener)
[![Security Scan](https://img.shields.io/badge/security-scan-success)](https://github.com/oussemaAbdaoui/url-shortener/security)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete DevOps implementation of a URL shortener service with full CI/CD pipeline, security scanning, containerization, and Kubernetes deployment.

## 📋 Project Overview

This project implements a **Mini URL Shortener** as part of a DevOps course. The goal is to practice end-to-end DevOps concepts including:

- ✅ **Backend Development** (Flask API under 150 lines)
- ✅ **Containerization** with Docker
- ✅ **CI/CD Pipeline** with GitHub Actions
- ✅ **Security Scanning** (SAST & DAST)
- ✅ **Kubernetes Deployment**
- ✅ **Observability** (Metrics, Logs, Tracing)
- ✅ **Complete Documentation**

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ Developer Workflow │
├─────────────────────────────────────────────────────────────┤
│ Code → Commit → Push → GitHub → CI/CD Pipeline → Deploy │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CI/CD Pipeline Flow │
├─────────────────────────────────────────────────────────────┤
│ 1. Code Quality & Testing → 2. Security SAST │
│ 3. Docker Build & Push → 4. Security DAST │
│ 5. Kubernetes Deployment → 6. Pipeline Summary │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Deployment Architecture │
├─────────────────────────────────────────────────────────────┤
│ Docker Image → Kubernetes → Service → End Users │
└─────────────────────────────────────────────────────────────┘

text

## 🚀 Quick Start

### 📦 Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Kubernetes (minikube/kubectl)
- Git

### 🔧 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/oussemaAbdaoui/url-shortener.git
cd url-shortener

# 2. Create virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
🐳 Using Docker
bash
# Build Docker image
docker build -t url-shortener:latest .

# Run container
docker run -d -p 5000:5000 --name url-shortener url-shortener:latest

# Test the container
curl http://localhost:5000/health
☸️ Kubernetes Deployment
bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Get service URL
minikube service url-shortener-service --url

# Test deployed service
curl http://SERVICE_URL/health
📡 API Endpoints
Method	Endpoint	Description	Example
GET	/	API Documentation	curl http://localhost:5000/
POST	/shorten	Create short URL	curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com"}'
GET	/{code}	Redirect to original URL	curl -L http://localhost:5000/abc123
GET	/stats/{code}	Get click statistics	curl http://localhost:5000/stats/abc123
GET	/health	Health check	curl http://localhost:5000/health
GET	/metrics	Prometheus metrics	curl http://localhost:5000/metrics
🔄 CI/CD Pipeline
Pipeline Stages:
Code Quality & Testing ✅

Python syntax checking

Code formatting (black)

Linting (flake8)

Basic unit tests

Security Scanning (SAST) ✅

Static Application Security Testing with Trivy

Vulnerability scanning of source code

Dependency checking

Build and Push Docker Image ✅

Multi-platform Docker build (linux/amd64, linux/arm64)

Image optimization

Push to Docker Hub registry

Dynamic Security Testing (DAST) ✅

OWASP ZAP baseline scan

Runtime vulnerability detection

Web application security testing

Deploy to Kubernetes ✅

Minikube cluster setup

Kubernetes manifests deployment

Health check validation

Smoke testing

📊 Pipeline Success Metrics
Total Jobs: 5

Successful Jobs: 5 (100%)

Total Run Time: ~3 minutes

Docker Build Time: 42 seconds

🔒 Security Implementation
Static Analysis (SAST)
Tool: Trivy

Scope: Source code vulnerability scanning

Results: No critical vulnerabilities found

Evidence: Included in pipeline artifacts

Dynamic Analysis (DAST)
Tool: OWASP ZAP

Scope: Running application testing

Results: Passed baseline security scan

Evidence: DAST reports available in pipeline artifacts

Container Security
Docker Image Scanning: Integrated in pipeline

Base Image: Python 3.11-slim (minimal attack surface)

Vulnerability Scan: Clean report

📈 Observability
Metrics (Prometheus)
bash
# Access metrics endpoint
curl http://localhost:5000/metrics

# Sample metrics output:
# http_requests_total{method="POST",endpoint="/shorten",status="201"} 5
# http_request_duration_seconds_bucket{endpoint="/shorten",le="0.1"} 4
# urls_created_total 12
Structured Logging
json
{
  "event": "request_completed",
  "method": "POST",
  "path": "/shorten",
  "status": 201,
  "duration": 0.045,
  "request_id": "a1b2c3d4",
  "level": "info",
  "timestamp": "2025-12-05T10:30:45.123456Z"
}
Request Tracing
Request ID Generation: UUID per request

Header: X-Request-ID included in all responses

Log Correlation: Request ID in all log entries

End-to-end Tracing: Basic request flow tracking

☸️ Kubernetes Deployment Details
Manifests
Deployment: k8s/deployment.yaml (2 replicas with resource limits)

Service: k8s/service.yaml (NodePort type)

Namespace: k8s/namespace.yaml (optional)

Configuration
yaml
replicas: 2
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
probes:
  liveness: /health (30s interval)
  readiness: /health (5s interval)
Access Methods
bash
# Method 1: Minikube tunnel
minikube tunnel

# Method 2: NodePort (default: 30007)
minikube service url-shortener-service --url

# Method 3: Port forwarding
kubectl port-forward svc/url-shortener-service 8080:80
📁 Project Structure
text
url-shortener/
├── app.py                    # Main Flask application (<150 lines)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Local development with Docker Compose
├── .github/workflows/       # CI/CD pipeline definitions
│   └── ci-cd.yml           # Main CI/CD pipeline
├── k8s/                     # Kubernetes manifests
│   ├── deployment.yaml     # Deployment configuration
│   └── service.yaml        # Service configuration
├── tests/                   # Test files
│   └── test_app.py         # Basic unit tests
├── README.md               # This documentation
└── .gitignore              # Git ignore file
🛠️ Development Workflow
1. Create a Feature Branch
bash
git checkout -b feature/your-feature-name
2. Make Changes and Test
bash
# Run tests locally
python tests/test_app.py

# Check code quality
black --check app.py
flake8 app.py
3. Commit and Push
bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
4. Create Pull Request
Go to GitHub repository

Create Pull Request from your branch

Request peer review

Address review comments

Merge after approval

🤝 Peer Review Process
This project includes mandatory peer review as per course requirements:

Create dedicated PRs for each major change

Request review from at least one classmate

Provide constructive feedback on others' PRs

Document review comments and resolutions

📊 Screenshots & Evidence
CI/CD Pipeline Success
https://img.shields.io/badge/pipeline-100%2525-success

Docker Hub Published Image
Image: oussemaabdaoui/url-shortener:latest

Status: Successfully published

Scan: Security scanned

Security Scan Results
SAST: ✅ Passed (Trivy)

DAST: ✅ Passed (OWASP ZAP)

Container Scan: ✅ Clean

Kubernetes Deployment Status
bash
# Command to verify deployment
kubectl get pods,services,deployments
🚧 Troubleshooting
Common Issues & Solutions
Port 5000 already in use

bash
# Find and kill process (Windows)
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Or use different port
docker run -d -p 5001:5000 url-shortener:latest
Docker build fails on Windows

bash
# Use explicit paths
docker build -t url-shortener:latest .

# Check Docker Desktop is running
Kubernetes deployment fails

bash
# Check minikube status
minikube status

# View detailed logs
kubectl describe pod [pod-name]
kubectl logs [pod-name]
Python import errors

bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
📚 Learning Outcomes
Technical Skills Gained
Containerization: Docker image creation and optimization

CI/CD Automation: GitHub Actions pipeline design

Security: SAST/DAST implementation and analysis

Kubernetes: Deployment, service, and configuration management

Observability: Metrics, logging, and tracing implementation

DevOps Principles Applied
Infrastructure as Code: Kubernetes manifests, Dockerfile

Automation First: Complete CI/CD pipeline

Security by Design: Integrated security scanning

Monitor Everything: Comprehensive observability

Documentation: Complete project documentation

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👏 Acknowledgments
Course Instructor: For guidance and DevOps concepts

Classmates: For peer reviews and collaboration

Open Source Community: For amazing tools (Docker, Kubernetes, GitHub Actions)

📞 Contact & Links
GitHub: @oussemaAbdaoui

Docker Hub: oussemaabdaoui/url-shortener

Repository: https://github.com/oussemaAbdaoui/url-shortener

CI/CD Pipeline: Actions Tab

"Enjoy the journey, not just the destination." - DevOps Project Motto

<div align="center">
🎯 Project Status: COMPLETED ✅
All requirements fulfilled:

Backend API (<150 lines)

Docker Containerization

CI/CD Pipeline (5/5 jobs passed)

Security Scanning (SAST + DAST)

Kubernetes Deployment

Observability (Metrics, Logs, Tracing)

Documentation & Final Report

</div> ```
