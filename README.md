# 🔥 Multi-Agent AI System

> Collaborative AI agents that research, analyze, and produce professional
> reports with real-time data insights

[![Deploy - Streamlit](https://img.shields.io/badge/Live_Demo-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://multi-agent-ai-system.onrender.com/)
[![API - FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](http://localhost:8000/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](docker-compose.yml)
[![OpenRouter AI](https://img.shields.io/badge/AI-OpenRouter-FF6B35?logo=openai&logoColor=white)](https://openrouter.ai/)
[![Llama 3.2](https://img.shields.io/badge/Model-Llama_3.2-0066CC?logo=meta&logoColor=white)](https://openrouter.ai/)

---

## Table of Contents

-   [Overview](#overview)
-   [Key Features](#key-features)
-   [Quick Start](#quick-start)
-   [User Interface](#user-interface)
-   [Enhanced Analytics](#enhanced-analytics)
-   [Technology Stack](#technology-stack)
-   [Project Structure](#project-structure)
-   [Configuration](#configuration)
-   [Deployment](#deployment)
-   [API Documentation](#api-documentation)
-   [Contributing](#contributing)
-   [License](#license)

---

## Overview

Multi-Agent AI System is a production-ready, collaborative AI platform where
specialized agents work together to deliver comprehensive research-driven
insights. The system combines the power of multiple AI agents with real-time
data analysis, advanced visualizations, and professional report generation.

### Perfect For:

-   **Market Research Analysts** - Get comprehensive stock analysis with
    predictions
-   **Business Intelligence Teams** - Generate detailed reports with data
    visualizations
-   **Data Scientists** - Access advanced statistical analysis and forecasting
-   **Developers** - Build upon a robust AI agent orchestration platform

---

## Key Features

### 🤖 Multi-Agent Architecture

-   **Research Agent**: Information gathering and data collection specialist
-   **Analysis Agent**: Pattern recognition and insight extraction expert
-   **Report Writer**: Professional documentation and summary generation
-   **Task Coordinator**: Workflow orchestration and result compilation

### 📊 Advanced Analytics Engine

-   **Real-time Data Processing**: Live market data, news, and web research
-   **Statistical Analysis**: Comprehensive statistical metrics and insights
-   **Predictive Modeling**: Market forecasting with confidence intervals
-   **Interactive Visualizations**: Plotly-powered charts and dashboards

### 🛠️ Developer-Friendly

-   **RESTful API**: FastAPI-powered backend with automatic OpenAPI docs
-   **Modular Design**: Clean, maintainable codebase with separated concerns
-   **Database Integration**: SQLAlchemy with SQLite/PostgreSQL support
-   **Async Processing**: High-performance concurrent task execution

### 💰 Cost-Effective & Flexible

-   **OpenRouter Integration**: Cloud AI with Llama 3.2 models (pay-per-use)
-   **Local LLM Support**: Optional Ollama integration for offline operation
-   **OpenAI Compatible**: Drop-in replacement for cloud AI services
-   **Docker Ready**: Containerized deployment for any environment

---

## Quick Start

### 🚀 **1-Click Docker Deployment (Easiest)**

```bash
# Get OpenRouter API key from https://openrouter.ai/
echo "OPENROUTER_API_KEY=your_api_key_here" > .env

# Deploy the AI system
docker run -d --name multi-agent-ai \
  -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  ghcr.io/rakeshsingh38/multi-agent-ai-system:latest

# Access at http://localhost:8501/
```

**✅ That's it!** Your AI system is running with Llama 3.2 and OpenRouter integration.

### 🛠️ **Local Development Setup**

#### Prerequisites

-   Python 3.9+
-   Git
-   Ollama (optional, for local LLMs)

#### 5-Minute Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/RakeshSingh38/multi-agent-ai-system.git
    cd multi-agent-ai-system
    ```

2. **Set up virtual environment**

    ```bash
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # Linux/Mac
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    # For full system (recommended)
    pip install -r requirements.txt
    ```

4. **Start the system**

    ```bash
    # Start API server (Terminal 1)
    python test_server.py

    # Start Streamlit UI (Terminal 2)
    streamlit run app.py
    ```

5. **Access the application**
    - Web UI: http://localhost:8501
    - API Docs: http://localhost:8000/docs
    - Live Demo:
      [Streamlit Cloud](https://multi-agent-ai-system.onrender.com/)

---

## User Interface

The application features a clean, modern interface with 5 main sections:

### 🚀 Research Tool

-   Custom Research: Enter any topic for comprehensive analysis
-   Quick Templates: Pre-built research templates for common topics
-   Real-time Progress: Live status updates during research
-   Question Builder: Add specific questions for targeted analysis

### 📊 Results

-   Research Summary: Key findings and insights
-   Data Sources: Links to original research sources
-   Q&A Section: Answers to your specific questions
-   Export Options: Download results in multiple formats

### 📈 Enhanced Analytics

-   Overview: Key metrics and market summary
-   Visualizations: Interactive charts and graphs
-   Predictions: Market forecasting and projections
-   Statistics: Advanced statistical analysis
-   Custom Analysis: Trend analysis and correlations

### 📖 About

-   System Information: Version, capabilities, and features
-   Documentation: Links to guides and resources
-   Support: Contact information and help resources

### 🛠️ Settings

-   Server Health: Real-time system status
-   API Configuration: Backend settings and endpoints
-   System Stats: Performance metrics and usage data
-   Quick Actions: System management tools

---

## Enhanced Analytics

### Overview Tab - Simplified

-   Key Findings: Extracted insights from research
-   Market Data Summary: Stock prices, changes, and metrics
-   Analysis Results: AI-generated insights and recommendations

### Visualizations Tab - Simplified

-   Market Sentiment Chart: Bullish/bearish sentiment analysis
-   Stock Price Comparison: Interactive multi-stock charts

### Predictions Tab - Simplified

-   3-Month Market Forecast: Future price projections
-   Volatility Analysis: Risk assessment and metrics

### Statistics Tab - Simplified

-   Market Overview: Comprehensive market metrics
-   Top Performers: Best and worst performing stocks

### Custom Analysis Tab - Simplified

-   Trend Analysis: Statistical trend detection with p-values
-   Correlation Analysis: Relationship detection between variables

---

## Technology Stack

| Component         | Technology                     | Purpose                   |
| ----------------- | ------------------------------ | ------------------------- |
| Backend           | FastAPI                        | High-performance REST API |
| Frontend          | Streamlit                      | Interactive web interface |
| AI/LLM            | Ollama, OpenAI                 | Language model processing |
| Database          | SQLAlchemy + SQLite/PostgreSQL | Data persistence          |
| Async Processing  | asyncio                        | Concurrent task execution |
| Data Analysis     | pandas, numpy, scipy           | Statistical computing     |
| Visualization     | Plotly                         | Interactive charts        |
| Machine Learning  | scikit-learn                   | Predictive modeling       |
| Containerization  | Docker                         | Deployment packaging      |
| API Documentation | OpenAPI/Swagger                | Auto-generated docs       |

---

## Project Structure

```
multi-agent-ai-system/
├── src/                          # Source code
│   ├── agents/                   # AI agent implementations
│   │   ├── agent_factory.py     # Agent creation factory
│   │   ├── analysis_agent.py    # Data analysis specialist
│   │   ├── base_agent.py        # Base agent class
│   │   ├── report_writer_agent.py # Report generation
│   │   ├── research_agent.py    # Research specialist
│   │   └── task_coordinator.py  # Workflow orchestration
│   ├── api/                     # FastAPI endpoints
│   │   ├── main.py              # API application
│   │   └── models.py            # Data models
│   ├── core/                    # Core utilities
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database layer
│   │   ├── logger.py            # Logging system
│   │   └── ollama_client.py     # Local LLM client
│   └── integrations/            # External integrations
├── pages/                        # Streamlit pages
│   ├── enhanced_results.py       # Enhanced analytics page
│   ├── research_tool.py          # Research interface
│   ├── results.py                # Results display
│   ├── settings.py               # Settings panel
│   ├── about.py                  # About page
│   ├── tabs/                     # Analytics tabs
│   └── components/               # UI components
├── tests/                        # Test suite
├── data/                         # Data storage
├── logs/                         # Application logs
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# LLM Configuration
LLM_BACKEND=ollama                    # ollama, openai, or huggingface
OLLAMA_MODEL=gemma2:2b               # Local model for Ollama
OPENAI_API_KEY=your_key_here         # For OpenAI backend
HUGGINGFACE_API_KEY=your_key_here    # For HuggingFace backend

# Database Configuration
DATABASE_URL=sqlite:///./multiagent.db  # SQLite (default)
# DATABASE_URL=postgresql://user:pass@localhost/dbname  # PostgreSQL

# API Configuration
API_HOST=localhost
API_PORT=8000

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
```

### LLM Backends

#### Ollama (Recommended - Free & Local)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull gemma2:2b
ollama pull mistral:latest
```

#### OpenAI (Cloud - Requires API Key)

```env
LLM_BACKEND=openai
OPENAI_API_KEY=sk-your-api-key-here
```

#### HuggingFace (Alternative Cloud)

```env
LLM_BACKEND=huggingface
HUGGINGFACE_API_KEY=hf-your-api-key-here
```

---

## Deployment

### Cloud Deployment

#### Streamlit Cloud (Easiest)

-   Deploy: Connect GitHub repo to Streamlit Cloud
-   URL: https://multi-agent-ai-system.onrender.com/
-   Cost: Free tier available

#### Railway/Render

```bash
# Use provided Dockerfile
git push origin main
# Deploy via Railway or Render dashboard
```

### Docker Deployment

#### 🚀 **OpenRouter Cloud Deployment (Recommended)**

**Production-ready with cloud AI inference:**

```bash
# Deploy from GitHub Container Registry
docker run -d --name multi-agent-ai \
  -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  ghcr.io/rakeshsingh38/multi-agent-ai-system:latest

# Alternative: Use OpenRouter-specific image
docker run -d --name multi-agent-openrouter \
  -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  ghcr.io/rakeshsingh38/multi-agent-openrouter:latest
```

**Features:**
- ✅ **OpenRouter Integration**: Cloud AI with Llama 3.2 3B model
- ✅ **Production Optimized**: 1.5GB lightweight image
- ✅ **High Performance**: Cloud inference (faster than local)
- ✅ **API Key Required**: Configure `OPENROUTER_API_KEY` in `.env`
- ✅ **Multi-Agent System**: Research, Analysis, and Report agents
- ✅ **Web UI + API**: Streamlit interface + FastAPI backend

**Environment Setup:**
```bash
# Create .env file with your OpenRouter API key
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
echo "OLLAMA_BASE_URL=https://openrouter.ai/api/v1" >> .env
echo "OLLAMA_MODEL=meta-llama/llama-3.2-3b-instruct" >> .env
```

#### 🏠 **Self-Contained Version (Offline)**

For offline deployments with built-in local AI model:

```bash
# Build self-contained image with local Ollama
# Windows
build-self-contained.bat

# Linux/Mac
chmod +x build-self-contained.sh
./build-self-contained.sh

# Run offline version
docker run -d -p 8000:8000 -p 8501:8501 -p 11434:11434 multi-agent-ai-self-contained
```

**Features:**
- ✅ **Offline Operation**: No internet required
- ✅ **Built-in Model**: Llama 3.2 1B local model
- ✅ **Self-Contained**: All dependencies included
- ❌ **Larger Size**: ~9.5GB image
- ❌ **Slower Performance**: Local inference

#### 🐳 **Local Development**

```bash
# Quick local development
docker-compose up --build

# Access at http://localhost:8501
```

#### ⚙️ **Production Docker Compose**

```bash
# Production deployment with reverse proxy
docker-compose -f docker-compose.prod.yml up -d
```

### 🚀 **Latest Deployment Commands (2025)**

#### **Quick Deploy (Recommended)**
```bash
# Deploy production-ready system with OpenRouter
docker run -d --name ai-system \
  -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  ghcr.io/rakeshsingh38/multi-agent-ai-system:latest

# Access your system:
# Web UI: http://localhost:8501/
# API: http://localhost:8000/
# Health: http://localhost:8000/health
```

#### **Alternative Deploy Options**
```bash
# Option 2: Use OpenRouter-specific image
docker run -d --name ai-openrouter \
  -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  ghcr.io/rakeshsingh38/multi-agent-openrouter:latest

# Option 3: Local development
docker-compose up --build
```

#### **Environment Configuration**
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
echo "OLLAMA_BASE_URL=https://openrouter.ai/api/v1" >> .env
echo "OLLAMA_MODEL=meta-llama/llama-3.2-3b-instruct" >> .env
echo "LLM_BACKEND=ollama" >> .env
```

#### **Management Commands**
```bash
# Check status
docker ps

# View logs
docker logs ai-system

# Stop system
docker stop ai-system

# Restart system
docker restart ai-system

# Update to latest version
docker pull ghcr.io/rakeshsingh38/multi-agent-ai-system:latest
docker stop ai-system
docker rm ai-system
# Then run deploy command above
```

### 📦 **Available Docker Images**

| Image | Size | AI Model | Internet | Use Case |
|-------|------|----------|----------|----------|
| `ghcr.io/rakeshsingh38/multi-agent-ai-system:latest` | 1.5GB | Llama 3.2 3B (OpenRouter) | ✅ Required | **Production Recommended** |
| `ghcr.io/rakeshsingh38/multi-agent-openrouter:latest` | 1.5GB | Llama 3.2 3B (OpenRouter) | ✅ Required | Production Alternative |
| `multi-agent-ai-self-contained:latest` | 9.5GB | Llama 3.2 1B (Local) | ❌ Offline | Offline/Isolated Deployments |

**🔥 Recommended:** Use OpenRouter images for best performance and reliability!

### Cloud Platforms

#### AWS/GCP/Azure

-   Container Ready: Use provided Dockerfile
-   Scalable: Auto-scaling based on load
-   CDN: Global content delivery

#### Heroku

```bash
# Heroku deployment
heroku create your-app-name
git push heroku main
```

---

## API Documentation

### REST Endpoints

#### Execute Task

```http
POST /tasks/execute
Content-Type: application/json

{
  "task_type": "full_analysis",
  "topic": "Impact of AI on Healthcare",
  "questions": [
    "What are the main applications?",
    "What are the challenges?",
    "What is the future outlook?"
  ],
  "report_type": "executive_summary",
  "target_audience": "technical"
}
```

#### Get Task Status

```http
GET /tasks/{task_id}
```

#### List Agents

```http
GET /agents
```

#### Health Check

```http
GET /health
```

### Python SDK Usage

```python
import requests

# Initialize client
BASE_URL = "http://localhost:8000"

# Execute research task
task_data = {
    "task_type": "full_analysis",
    "topic": "Analyze Apple, Microsoft, Google stocks",
    "questions": [
        "What are the current stock prices?",
        "What is the market sentiment?",
        "What are the future predictions?"
    ],
    "report_type": "comprehensive",
    "target_audience": "investors"
}

# Submit task
response = requests.post(f"{BASE_URL}/tasks/execute", json=task_data)
result = response.json()

print(f"Task ID: {result['task_id']}")
print(f"Status: {result['status']}")

# Check results
task_response = requests.get(f"{BASE_URL}/tasks/{result['task_id']}")
final_result = task_response.json()
```

---

## Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

1. Fork the repository
2. Clone your fork:
   `git clone https://github.com/RakeshSingh38/multi-agent-ai-system.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test thoroughly: `pytest tests/`
6. Commit your changes: `git commit -m "Add amazing feature"`
7. Push to your branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Standards

-   Formatting: Black code formatter
-   Linting: flake8 with max line length 88
-   Testing: pytest with minimum 80% coverage
-   Documentation: Google-style docstrings

### Areas for Contribution

-   New Agents: Specialized AI agents for specific domains
-   Enhanced Analytics: Additional visualization types
-   API Integrations: Third-party service integrations
-   Performance Optimization: Async processing improvements
-   Documentation: Tutorials, guides, and examples

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

---

## Acknowledgments

### Core Technologies

-   FastAPI: Lightning-fast API framework
-   Streamlit: Beautiful web apps with Python
-   Ollama: Local LLM inference made easy
-   Plotly: Interactive data visualizations

### Inspiration

-   AutoGPT: Multi-agent AI architectures
-   LangChain: LLM application frameworks
-   CrewAI: Agent orchestration patterns

### Contributors

-   Rakesh Singh: Project creator and maintainer
-   Open Source Community: Bug reports, feature requests, and contributions

---

### Main Dashboard

_[Screenshot of main interface with navigation tabs]_

### Research Tool

_[Screenshot of research input form with templates]_

### Enhanced Analytics - Overview

_[Screenshot of overview tab with key metrics]_

### Enhanced Analytics - Visualizations

_[Screenshot of interactive charts and graphs]_

### Enhanced Analytics - Predictions

_[Screenshot of market forecasting dashboard]_

### API Documentation

_[Screenshot of Swagger/OpenAPI documentation]_

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

_Built with ❤️ using cutting-edge AI and modern Python technologies_

---

### 📊 **Current System Status (October 2025)**

✅ **Fully Operational Features:**
- Multi-agent AI system with Research, Analysis, and Report agents
- OpenRouter integration with Llama 3.2 3B model
- Real-time data collection from web sources
- Professional report generation
- Streamlit web interface + FastAPI backend
- Docker containerization ready
- Production deployment on GHCR

✅ **Available Deployments:**
- **GitHub Container Registry**: `ghcr.io/rakeshsingh38/multi-agent-ai-system:latest`
- **Alternative**: `ghcr.io/rakeshsingh38/multi-agent-openrouter:latest`
- **Local Development**: Docker Compose setup

✅ **Tested & Verified:**
- OpenRouter API integration working
- All agents functioning correctly
- Web interface operational
- API endpoints responding
- Health checks passing

🔥 **Ready for Production Use!**
