#!/bin/bash
# Frontend Package Setup
node_directory="../frontend";
docker_directory="../docker";
cd $node_directory;
npm install -g npm@latest;
npm update;
# Docker Setups
sudo docker compose -f /home/student68/FerrisWheel_3/FerrisWheel/docker/docker-compose.yaml down frontend backend;
sudo docker builder prune -f;
sudo docker image prune -f;
sudo docker compose -f /home/student68/FerrisWheel_3/FerrisWheel/docker/docker-compose.yaml build frontend backend;
sudo docker compose -f /home/student68/FerrisWheel_3/FerrisWheel/docker/docker-compose.yaml up -d frontend backend;

