#!/bin/bash
echo "Cleaning up Docker resources..."
docker-compose down --volumes --remove-orphans
docker network prune -f
echo "Building and starting Docker containers..."
docker-compose up --build
