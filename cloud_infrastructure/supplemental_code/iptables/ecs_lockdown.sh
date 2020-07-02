#!/usr/bin/env bash
# *************************************************************************************************
# ecs-lockdown.sh - Enable Lockdown on ECS Nodes to prevent containers from accessing the Node
#                   Metadata
#
# Variables required to be provided from the environment (provisioner)
#   NONE
#
# Secrets required to be present in the provided AWS Secret
#   NONE
#
# Required External Scripts
#   NONE
#
# *************************************************************************************************
# This requires iptables-services (not installed by default)
sudo yum install -y iptables-services
# DOCKER-USER table - block connections to 169.254.169.254
# Block all external traffic but allow VPC traffic from containers
# change the 10.0.0.0/8 to match your trusted VPC CIDR
sudo iptables --insert DOCKER-USER --in-interface docker0 -o eth0 -j DROP
sudo iptables --insert DOCKER-USER --in-interface docker0 -o eth0 -d 10.0.0.0/8 -j RETURN
# From https://ops.tips/blog/blocking-docker-containers-from-ec2-metadata/
sudo iptables --insert DOCKER-USER --destination 169.254.169.254 --jump REJECT --reject-with icmp-port-unreachable
# Allow access to tinyproxy on 172.17.0.1, but "fake block" all other traffic (redirect to port 2)
sudo iptables -t nat -A PREROUTING -i docker0 -d 172.17.0.1 -p tcp --dport 8888 -j RETURN
sudo iptables -t nat -A PREROUTING -i docker0 -d 172.17.0.1 -p tcp -j DNAT --to-destination :2
# Save the configuration
# NOTE: make sure this is done close to the end of the image build to make sure all the
#       docker managed rules are properly in place.
sudo bash -c "iptables-save > iptables"
sudo install -m 600 iptables /etc/sysconfig/iptables
sudo rm iptables
sudo systemctl enable --now iptables 2>&1
# Install Enterprise TLS Inspecting Gateway Proxy Certificate
if [[ -f trusted_enterprise.crt ]]; then
  sudo install -m 644 trusted_enterprise.crt /etc/pki/ca-trust/source/anchors/
  rm trusted_enterprise.crt
  sudo update-ca-trust
fi
# Disable icc
echo -e '{\n  "icc": false\n}\n' >> daemon.json
sudo install -m 644 daemon.json /etc/docker/daemon.json
rm daemon.json
echo "Docker daemon.json:"
cat /etc/docker/daemon.json
# Disable containers running with awsvpc networking from accessing the node credentials
sudo bash -c "echo ECS_AWSVPC_BLOCK_IMDS=true >> /etc/ecs/ecs.config"
sudo bash -c "echo ECS_RESERVED_MEMORY=1024 >> /etc/ecs/ecs.config"
echo "ECS Config:"
cat /etc/ecs/ecs.config