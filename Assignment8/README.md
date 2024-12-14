# LLM Operations Platform

This project demonstrates a comprehensive end-to-end Large Language Model (LLM) Operations workflow. It showcases best practices in building and deploying GenAI applications, including data preparation, model training, deployment, monitoring, and user interaction.

# Demo Video
  [Drive link](https://drive.google.com/drive/folders/1dCZ5Gw3OuPJOUU467JhJ6Iv_5UvYh-qT?usp=sharing)

## Features

### 1. Data Pipeline
- Automated data preprocessing and validation
- Dataset versioning and quality metrics
- Configurable data transformation workflows
- Progress tracking and error handling

### 2. Model Operations
- Model training and fine-tuning pipeline
- Model versioning and registry
- Performance evaluation metrics
- A/B testing capabilities

### 3. Deployment Infrastructure
- FastAPI backend service
- React frontend interface
- Model serving with versioning
- Real-time inference endpoints

### 4. Monitoring & Logging
- Real-time performance metrics
- System resource monitoring
- Error tracking and alerting
- Prometheus integration

## Project Structure

```
llm-ops-demo/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes and endpoints
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Data models and schemas
│   │   └── services/     # Business logic services
│   ├── tests/            # Unit and integration tests
│   └── Dockerfile        # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   └── services/     # API integration
│   ├── public/           # Static assets
│   └── Dockerfile        # Frontend container configuration
├── data/
│   ├── raw/              # Raw data storage
│   └── processed/        # Processed datasets
├── models/               # Model artifacts and configs
├── docker-compose.yml    # Docker services orchestration
└── prometheus.yml        # Prometheus monitoring config
```

## Prerequisites

1. Docker and Docker Compose
2. Git (for cloning the repository)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-ops-demo.git
cd llm-ops-demo
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

This will start:
- Frontend service at http://localhost:3000
- Backend API at http://localhost:8000
- Prometheus metrics at http://localhost:9090

## Accessing the Application

### Frontend Interface
- Main application: http://localhost:3000
- Features:
  - Interactive model inference
  - Real-time monitoring dashboard
  - Data pipeline visualization
  - System metrics and logs

### Backend API
- API documentation: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Monitoring
- Prometheus metrics: http://localhost:9090
- System metrics and model performance monitoring

## Key Components

### 1. Data Processing Pipeline
- Automated data validation and cleaning
- Quality metrics calculation
- Dataset versioning
- Progress tracking

### 2. Model Training
- Fine-tuning pipeline
- Hyperparameter optimization
- Model evaluation
- Version control

### 3. Inference API
- Real-time predictions
- Batch processing
- Model versioning
- Error handling

### 4. Monitoring Dashboard
- Real-time metrics
- System health monitoring
- Error tracking
- Performance analytics

## API Endpoints

### Model Operations
- `POST /api/predict`: Make predictions
- `GET /api/model/health`: Check model health
- `GET /api/metrics`: Get performance metrics

### Data Pipeline
- `POST /api/data/process`: Process new data
- `GET /api/data/status`: Check processing status
- `GET /api/data/metrics`: Get data quality metrics

### Monitoring
- `GET /health`: System health check
- `GET /metrics`: Prometheus metrics

## Development

### Running Tests
```bash
# Backend tests (inside backend container)
docker-compose exec backend pytest

# Frontend tests (inside frontend container)
docker-compose exec frontend npm test
```

### Viewing Logs
```bash
# View all services
docker-compose logs

# View specific service
docker-compose logs backend
docker-compose logs frontend
```

### Rebuilding Services
```bash
# Rebuild specific service
docker-compose up -d --build backend
docker-compose up -d --build frontend

# Rebuild all services
docker-compose up -d --build
```

## Production Deployment

For production deployment:

1. Update environment variables in docker-compose.yml
2. Configure proper security measures
3. Set up proper monitoring and logging
4. Use production-grade servers
5. Implement proper backup strategies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
