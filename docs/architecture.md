# Architecture

## Current deployed architecture

This project serves a Hugging Face sentiment-analysis model through a FastAPI API running in Azure Container Apps. Terraform provisions the Azure resources.

```mermaid
flowchart LR
    developer[Developer]
    source[Application source\nFastAPI + Transformers]
    docker[Docker build\nPre-downloads model]
    registry[Azure Container Registry\nsentiment-api:v1]
    terraform[Terraform\nInfrastructure as code]
    azure[Azure Resource Group]
    environment[Container Apps Environment]
    app[Container App\nsentiment-api\n0.5 vCPU / 1 GiB\n1-2 replicas]
    api[Public HTTPS endpoint\n/health and /predict]
    client[API client]
    model[Sentiment model\nloaded once at startup]
    insights[Application Insights]
    logs[Log Analytics Workspace]
    vault[Key Vault\nProvisioned for secrets]

    developer --> source
    source --> docker
    docker --> registry
    registry --> app

    terraform --> azure
    azure --> registry
    azure --> vault
    azure --> logs
    azure --> insights
    azure --> environment
    environment --> app

    client --> api
    api --> app
    app --> model
    app --> insights
    insights --> logs

    classDef client fill:#e8f1ff,stroke:#2563eb,color:#0f172a
    classDef build fill:#fff4d6,stroke:#d97706,color:#0f172a
    classDef azure fill:#e8f7ee,stroke:#16803c,color:#0f172a
    classDef runtime fill:#f3e8ff,stroke:#7e22ce,color:#0f172a
    classDef observability fill:#ffe8e8,stroke:#dc2626,color:#0f172a

    class developer,client,api client
    class source,docker,terraform build
    class registry,azure,environment,vault azure
    class app,model runtime
    class insights,logs observability
```

## Runtime request flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant I as Container Apps ingress
    participant A as FastAPI container
    participant M as Sentiment model
    participant O as Application Insights

    C->>I: POST /predict with text
    I->>A: Forward request to port 8000
    A->>M: Classify text
    M-->>A: Label and confidence score
    A-->>I: JSON response
    I-->>C: 200 OK
    A->>O: Application telemetry
```

## What is deployed today

- FastAPI inference service with `/health` and `/predict`
- Docker image stored in Azure Container Registry
- Azure Container App with external HTTPS ingress
- Autoscaling range of 1 to 2 replicas
- Application Insights connected to Log Analytics
- Key Vault resource provisioned for future secret-management work
- Terraform-managed Azure infrastructure

## Important scope note

The current project is an ML inference API, not an LLM chat application. The next roadmap phase can add an LLM serving layer, followed by RAG, evaluation, monitoring, and cost controls.
