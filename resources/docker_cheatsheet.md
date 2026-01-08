# Docker CLI Cheat Sheet

| **Command Description**                                                  | **Command**                                                             |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Build an image from a Dockerfile                                         | `docker build -t <image_name> .`                                        |
| Build an image without using the cache                                   | `docker build -t <image_name> . --no-cache`                             |
| List local Docker images                                                 | `docker images`                                                         |
| Delete an image                                                          | `docker rmi <image_name>`                                               |
| Remove all unused images                                                 | `docker image prune`                                                    |
| Log in to Docker Hub                                                     | `docker login -u <username>`                                            |
| Publish an image to Docker Hub                                           | `docker push <username>/<image_name>`                                   |
| Search Docker Hub for an image                                           | `docker search <image_name>`                                            |
| Pull an image from Docker Hub                                            | `docker pull <image_name>`                                              |
| Create and run a container from an image with a custom name              | `docker run --name <container_name> <image_name>`                       |
| Run a container and publish its port(s) to the host                      | `docker run -p <host_port>:<container_port> <image_name>`               |
| Run a container in the background (detached mode)                        | `docker run -d <image_name>`                                            |
| Start or stop an existing container                                      | `docker start|stop <container_name>`                                    |
| Remove a stopped container                                               | `docker rm <container_name>`                                            |
| Open a shell inside a running container                                  | `docker exec -it <container_name> sh`                                   |
| Fetch and follow logs of a container                                     | `docker logs -f <container_name>`                                       |
| Inspect details of a running container                                   | `docker inspect <container_name>`                                       |
| List currently running containers                                        | `docker ps`                                                             |
| List all containers (running and stopped)                                | `docker ps --all`                                                       |
| View resource usage statistics                                           | `docker container stats`                                                |
| Start the Docker daemon                                                  | `docker -d`                                                             |
| Get help with Docker or any subcommand                                   | `docker --help`                                                         |
| Display system-wide information                                          | `docker info`                                                           |
