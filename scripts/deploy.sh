#!/usr/bin/env bash
set -e

echo "========================================================================="
echo "       VIDEO INTELLIGENCE PLATFORM - ENTERPRISE DEPLOYMENT SCRIPT        "
echo "========================================================================="

echo "[1/3] Running Automated Test Suite..."
python tests/test_enterprise_suite.py

echo "[2/3] Building Docker Containers..."
docker-compose build

echo "[3/3] Launching Production Stack..."
docker-compose up -d

echo "Deployment complete! API available at http://localhost:8000/health"
