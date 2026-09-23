# Azure MLOps Sentiment API

A production-style machine-learning inference API built with FastAPI, Docker, Terraform, and Azure Container Apps.

The service accepts text and returns a sentiment label with a confidence score using a Hugging Face Transformers model.

## Live API

- Swagger documentation: https://sentiment-api.icysea-3dc18b81.eastus.azurecontainerapps.io/docs
- Health check: https://sentiment-api.icysea-3dc18b81.eastus.azurecontainerapps.io/health
- Prediction endpoint: `POST /predict`

Example request:

```bash
curl -X POST "https://sentiment-api.icysea-3dc18b81.eastus.azurecontainerapps.io/predict" \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this deployment"}'
```

Example response:

```json
{
  "label": "POSITIVE",
  "score": 0.99
}
```

## Architecture

See the [architecture documentation](docs/architecture.md) for the rendered Mermaid diagrams.

The architecture documentation includes:

- Application build and deployment flow
- Terraform-managed Azure resources
- Runtime request sequence
- Container Registry and Container Apps flow
- Application Insights and Log Analytics integration

## Technology stack

- Python 3.11
- FastAPI
- Uvicorn
- Hugging Face Transformers
- PyTorch CPU
- Docker
- Terraform
- Azure Container Registry
- Azure Container Apps
- Application Insights
- Log Analytics

## Project structure

```text
.
├── app/
│   ├── main.py          # FastAPI application and model inference endpoint
│   └── test_model.py    # Model smoke test
├── infra/
│   ├── main.tf          # Azure infrastructure
│   └── .terraform.lock.hcl
├── docs/
│   └── architecture.md # Mermaid architecture diagrams
├── Dockerfile
├── requirements.txt
└── LICENSE
```

## Run locally

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the local API documentation at http://localhost:8000/docs.

## Run with Docker

Build the image:

```bash
docker build -t sentiment-api:v1 .
```

Run the container:

```bash
docker run --rm -p 8000:8000 sentiment-api:v1
```

The Docker build downloads the sentiment model into the image so the container does not need to download it on every restart.

## Deploy with Terraform

Authenticate with Azure and make sure the target subscription is selected:

```bash
az login
az account set --subscription "<subscription-id>"
```

Build and push the image required by the Terraform configuration:

```bash
docker build -t acrmlops1rafey.azurecr.io/sentiment-api:v1 .
az acr login --name acrmlops1rafey
docker push acrmlops1rafey.azurecr.io/sentiment-api:v1
```

Initialize and validate Terraform:

```bash
cd infra
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Terraform provisions the resource group, container registry, Key Vault, Log Analytics workspace, Application Insights, Container Apps environment, and Container App.

Do not commit Terraform state, credentials, or secrets. The repository ignores Terraform state and local environment files.

## Current scope

This project is an ML inference API, not a chat application or LLM service. It demonstrates the foundation for serving a model through a cloud-hosted API with infrastructure as code.

## Roadmap

- Production LLM inference with an open-weight model and vLLM
- GPU-backed serving on Azure
- Secrets and private networking through Key Vault and API Management
- RAG ingestion, embeddings, vector search, and evaluation
- CI/CD with automated quality gates
- Model, latency, token, and cost monitoring dashboards

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
