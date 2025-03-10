# Summarize App - Ai 

This README provides a step-by-step guide to set up NVIDIA Docker, build the `summarize-app` container, and run it on an Ubuntu machine. Please note that GPU support requires an NVIDIA GPU and the necessary drivers installed on the host machine.

## Prerequisites

1. **Ubuntu Operating System**: Ensure you are running Ubuntu.
2. **NVIDIA GPU**: A supported NVIDIA GPU must be present on your machine.
3. **Docker**: Ensure Docker is installed on your system. If not, install Docker by following the [official Docker installation guide](https://docs.docker.com/engine/install/ubuntu/).
4. **NVIDIA Drivers**: Install the appropriate NVIDIA drivers for your GPU. You can verify the installation with:
   ```bash
   nvidia-smi
   ```
5. **nvidia-container-toolkit**: This guide includes steps to install the toolkit required for running containers with GPU support.
6. **Dockerfile and Setup Script**: Ensure you have the `Dockerfile` and `setup.sh` files for building the application.

## Steps to Install NVIDIA Docker, Build, and Run the Application

### 1. Add NVIDIA Docker Repository and GPG Key

Run the following commands to add the NVIDIA Docker GPG key and repository:

```bash
curl -s -L nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$( . /etc/os-release; echo $ID$VERSION_ID )
curl -s -L nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

### 2. Update Package List

Refresh the package list to include the newly added NVIDIA Docker repository:

```bash
sudo apt-get update
```

### 3. Install NVIDIA Docker Toolkit

Install `nvidia-docker2` and reload the Docker configuration:

```bash
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
```

### 4. Build the Docker Image

Use the provided `Dockerfile` to build the `summarize-app` image. Ensure the `setup.sh` script is included in the same directory as the `Dockerfile`.

Run the following command to build the image:

```bash
docker build -t summarize-app .
```

This command will execute the instructions in the `Dockerfile`, including running the `setup.sh` script to set up the application environment.

### 5. Run the Summarize-App Container

Run the `summarize-app` container using the following command:

```bash
docker run --runtime=nvidia --gpus all -p 5000:5000 summarize-app
```

This command:
- Enables GPU support with `--runtime=nvidia` and `--gpus all`.
- Maps port `5000` of the container to port `5000` on the host machine.

### 6. Access the Application

Once the container is running, you can access the application in your web browser at:

```
http://<your-server-ip>:5000
```

Replace `<your-server-ip>` with `localhost` or the IP address of your Ubuntu machine.

## Notes

- **GPU Requirement**: This setup is designed for systems with an NVIDIA GPU. Without a GPU, the application will not function as intended.
- **Dockerfile and Setup Script**: Ensure the `setup.sh` script is correctly configured and referenced in the `Dockerfile` to avoid build errors.
- **Compatibility**: Ensure your Docker version and NVIDIA drivers are compatible with the `nvidia-docker2` package.

For more information, visit the [NVIDIA Docker GitHub repository](https://github.com/NVIDIA/nvidia-docker).