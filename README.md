#  knack-legit

A legacy-friendly interface for publishing data to [Knack](http://knack.com) applications.

## Why?

Some legacy systems don't integrate well with "modern" applications. Legacy systems might require a self-signed SSL certificate, or a static IP address in order to communicate with others. They may even require your downstream application to be on the same network!

Knack-legit cures these headaches by acting as a legit intermediary between fussy legacy systems and Knack. It is intended to be launched locally, where it can pass requests from your legacy system to Knack. Your legacy system will never know the difference!

##  Quick Start

1. Install [Docker](https://docs.docker.com/) and launch the Docker engine on your host: `systemctl start docker`.

2. Build the Docker image: `docker build -t flask-restful .`.

3. Clone this repo to your host and `cd` into it: `git clone http://github.com/cityofaustin/cctv-serivce && cd knack-legacy`.

4. Configure `secrets.py` with your Flask app's [secret key](http://flask.pocoo.org/docs/0.12/quickstart/#sessions).

5. (Optionally) Deposit SSL certificates in the root directory and provide `key.pem` to your client:  `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

6. Launch the container/app: 

```
sudo docker run -d \
    -p 5002:5002 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    --rm \
    flask-restful
```

7. PUT records to `http://[Your host IP]:5002/objects/{ your object_key/records`

## Tests

1. Add your [Knack app ID api key](https://www.knack.com/developer-documentation/#object-based-post) to `secrets.py`  

2. Update `test.py` with your Knack app's object_key and record data.

3. Run `python test.py` to send your PUT request.

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).