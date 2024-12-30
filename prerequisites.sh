#Setting the GPG and remote repo for the package:
curl -s -L nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
# Save that file and refresh the package list
sudo apt-get update
# Install nvidia-docker2 and reload the Docker configurations
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
