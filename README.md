# Gemini Chatbot

A simple chatbot application powered by Google's Gemini API, built with Streamlit and ready for Docker/Kubernetes deployment.

## Features

- Clean and intuitive UI
- Real-time chat with Google Gemini AI
- Adjustable temperature and token settings
- Chat history management
- Containerized deployment ready
- Kubernetes manifests included

## Prerequisites

- Python 3.11+
- Docker (for containerization)
- Kubernetes cluster (for K8s deployment)
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Quick Start (Local Development)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here
streamlit run app.py

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Docker Deployment

### Build the Docker Image

```bash
docker build -t gemini-chatbot:latest .
```

### Run with Docker

```bash
docker run -p 8501:8501 -e GEMINI_API_KEY=your_api_key_here gemini-chatbot:latest
```

Access the app at `http://localhost:8501`

### Using Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

## Kubernetes Deployment

### 1. Update the Secret

Edit `k8s/secret.yaml` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key.

### 2. Build and Load Docker Image

```bash
# Build the image
docker build -t gemini-chatbot:latest .

# For Minikube
minikube image load gemini-chatbot:latest

# For Kind
kind load docker-image gemini-chatbot:latest

# For remote cluster, push to registry
docker tag gemini-chatbot:latest your-registry/gemini-chatbot:latest
docker push your-registry/gemini-chatbot:latest
```

### 3. Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4. Check Deployment Status

```bash
# Check pods
kubectl get pods

# Check service
kubectl get svc gemini-chatbot-service

# Get logs
kubectl logs -l app=gemini-chatbot
```

### 5. Access the Application

```bash
# For LoadBalancer service
kubectl get svc gemini-chatbot-service

# For Minikube
minikube service gemini-chatbot-service

# For port-forward (development)
kubectl port-forward svc/gemini-chatbot-service 8501:8501
```

Then access at `http://localhost:8501`

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── .dockerignore          # Docker ignore patterns
├── .env.example           # Environment variables template
├── README.md              # This file
└── k8s/                   # Kubernetes manifests
    ├── secret.yaml        # API key secret
    ├── deployment.yaml    # Application deployment
    └── service.yaml       # LoadBalancer service
```

## Configuration

### Application Settings

- **Temperature**: Controls randomness (0.0 = focused, 1.0 = creative)
- **Max Tokens**: Maximum response length (100-2000)

### Kubernetes Resources

Default resource limits in deployment:
- Requests: 256Mi memory, 250m CPU
- Limits: 512Mi memory, 500m CPU

Adjust in `k8s/deployment.yaml` as needed.

## Troubleshooting

### API Key Issues

```bash
# Check if secret is created
kubectl get secret gemini-api-secret

# Verify secret content (base64 encoded)
kubectl get secret gemini-api-secret -o yaml
```

### Pod Issues

```bash
# Check pod status
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
```

### Service Issues

```bash
# Check endpoints
kubectl get endpoints gemini-chatbot-service

# Test service connectivity
kubectl run test-pod --rm -it --image=curlimages/curl -- sh
curl http://gemini-chatbot-service:8501/_stcore/health
```

## Security Notes

- Never commit your `.env` file or actual API keys
- Use Kubernetes secrets for production deployments
- Consider using external secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
- Implement proper RBAC for Kubernetes deployments

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues and questions:
- Google Gemini API: [Documentation](https://ai.google.dev/docs)
- Streamlit: [Documentation](https://docs.streamlit.io)
