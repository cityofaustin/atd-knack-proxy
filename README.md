#  esb-knack

An API interface for publishing data to Knack from the Enterprise Service Bus (ESB).

## Why?

Corporate IT provides the Enterprise Service Bus (ESB) as a tool to integrate data between enterprise applications. Notably, the ESB serves as the primary mechanism by which the 311 CSR system communicates with other City of Austin applications. 

Although the ESB can integrate with Knack, the ESB requires static SSL certificates and prefers static IP addresses. Esb-knack cures these headaches by acting as an intermediary between the ESB and Knack. It parses POST requests from the ESB and passes these requests to Knack, returning all responses to the ESB in kind.

This interface is designed to run on a machine with a static IP sitting behind the City of Austin firewall, but it will handle any valid Knack POST from any sender. Maybe you can find another use for it.

##  Quick Start

1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Configure `secrets.py` with your Flask app's secret key and your Knack app credentials

4. (Optional) Create self-signed certs (clients will need `key.pem`):  `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

5. Build the Docker image: `docker build -t flask-restful .`.

6. Launch the container/app: 

```
sudo docker run -d \
    -p 5002:5002 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    --rm \
    flask-restful
```

7. Post records to `http://[Your host IP]:5002/objects/{ your object_key/records`

## Tests

1. Configure `secrets.py` with your Flask app's secret key and your Knack app credentials

2. Update `test.py` with your application's object_key and appropriate record.

3. Run `python test.py` to post your record.


