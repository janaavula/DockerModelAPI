# Deploy a model as a docker image (With nginx, gunicorn , flask , keras model ) and start a docker container

- Install Docker
- docker build -t predict-service . 
- docker run -p 80:80 -t predict-service
- docker run -it predict-service /bin/bash for troubleshooting in bash
-  docker images
- docker ps -a
- look at the images folder for docker settings and postman settings

- To upload large files https://git-lfs.github.com/
