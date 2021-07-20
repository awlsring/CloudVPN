#!/bin/bash

# Update system
sudo apt update -y
sudo apt upgrade -y

# Install system dependencies
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add docker repo
echo \
  "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update and install docker and friends
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Get docker-compose
sudo curl -L --fail https://raw.githubusercontent.com/linuxserver/docker-docker-compose/master/run.sh -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Make resting dirs
sudo mkdir -p /wireguard/config
sudo mkdir -p /wireguard/lib/modules

# Start container
docker-compose up -d