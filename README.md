#  knack-proxy

A legacy-friendly interface for publishing data to [Knack](http://knack.com) applications.

## Why?

Some legacy systems don't integrate well with "modern" applications. Legacy systems might require a self-signed SSL certificate or a static IP address in order to communicate with others. They may even require your downstream application to be on the same network!

Knack-proxy cures these headaches by acting as an intermediary between fussy legacy systems and Knack. Your legacy system will never know the difference!

##  Quick Start

1. Install [Docker](https://docs.docker.com/) and launch the Docker engine on your host: `systemctl start docker`.

2. Build the Nginx Docker image: `docker build -t atddocker/knack-proxy-nginx -f Dockerfile-knack-proxy-nginx .`.

3. Build the Gunicorn + Flask Docker image: `docker build -t atddocker/knack-proxy-flask -f Dockerfile-knack-proxy-flask  .`.

4. Create a docker [bridge network](https://docs.docker.com/network/network-tutorial-standalone/): `docker network create --subnet=172.18.0.0/16 my-net`.

5. Clone this repo to your host and `cd` into it: `git clone http://github.com/cityofaustin/knack-proxy && cd knack-proxy`.

6. Generate SSL certificates in the root directory:  `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

7. You'll launch two Nginx containers:

HTTP (port 80)
```bash
docker run -it --name nginx-80 \
    -d \
    --rm \
    --network my-net \
    -p 80:80 \
    -v "$(pwd)":/app/ atddocker/knack-proxy-nginx
```

HTTPS (port 443):
```bash
docker run -it --name nginx-443 \
    -d \
    --rm \
    --network my-net \
    -p 443:443 \
    -v "$(pwd)":/app/ atddocker/knack-proxy-nginx
```

8. Run Gunicorn + Flask container to launch the Knack-Proxy app. Note how we've given our app container a static IP so the Nginx can pass requests to it:

```bash
docker run -it --name knack-proxy-flask \
    -d \
    --rm \
    --network my-net \
    --ip 172.18.0.22 \
    -v "$(pwd)":/app/ \
    atddocker/knack-proxy-flask
```

9. Verify your three containers are running: `docker ps`.

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
418f0a2ab0fe        flask-restful       "python /usr/local..."   15 minutes ago      Up 15 minutes                              my-flask
b1a4884efb9f        nginx-custom        "nginx -g 'daemon ..."   16 minutes ago      Up 16 minutes       0.0.0.0:443->443/tcp   my-nginx-ssl
e8d45397fea2        nginx-custom        "nginx -g 'daemon ..."   27 minutes ago      Up 27 minutes       0.0.0.0:80->80/tcp     my-nginx
```

10. You're all set! POST Knack records to `http://[Your host IP]/v1/objects/{ your_object_key }/records`

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
