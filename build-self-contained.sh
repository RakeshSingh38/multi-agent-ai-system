#!/bin/bash
echo "Building Multi-Agent AI System with Built-in Ollama Model..."
echo "This will download and include Ollama with gemma2:2b model (~2GB)"
echo ""

docker build -f Dockerfile.self-contained -t multi-agent-ai-self-contained .

echo ""
echo "Build complete! Run with:"
echo "docker run -d -p 8000:8000 -p 8501:8501 -p 11434:11434 multi-agent-ai-self-contained"
echo ""
echo "Or use docker-compose:"
echo "docker-compose -f docker-compose.self-contained.yml up -d"