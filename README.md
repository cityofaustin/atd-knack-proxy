#  esb-knack
An API interface for publishing data to Knack from the Enterprise Service Bus (ESB).

##  Quick Start
1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Build the Docker image: `docker build -t flask-restful .`.

4. Launch the container/app: 

```
sudo docker run -d \
    -p 5002:5002 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    --rm \
    flask-restful
```

5. Visit the app at `http://[Your host IP]:5002`