#  knack-proxy

A legacy-friendly interface for publishing data to [Knack](http://knack.com) applications.

## Why?

Some legacy systems don't integrate well with "modern" applications. Legacy systems might require a self-signed SSL certificate or a static IP address in order to communicate with others. They may even require your downstream application to be on the same network!

Knack-proxy cures these headaches by acting as an intermediary between fussy legacy systems and Knack. Your legacy system will never know the difference!

## Deployment

This package can deploy on an AWS Lambda function through zappa, for details on how to utilize this framework refer to their documentation here: [https://github.com/Miserlou/Zappa](https://github.com/Miserlou/Zappa)

1. Create a virtual environment: `virtualenv venv`
2. Load the virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run these commands:

Take a look at the `zappa_settings.json` file, it includes the necessary configuration to deploy your function. In the configuration file, there are two environments, one for production and another for development. For the sake of this example, let's say we want to deploy/update production:

- If NOT deployed use:

```bash
zappa deploy production
``` 
 
- If already deployed and making an update:

```bash
zappa update production
```

- If you want to get rid of the function:

```bash
zappa undeploy production
```

### Testing & Development

When implementing new code, there are multiple ways to test things:
1. Run the server locally, e.g.: `python3 __init__.py`
2. Run the script as a docker container (as described in the quick start steps)

### Deployment Pipeline, Development Lifecycle

The pipeline is at the moment very simple given the nature of this project; however, there is space for development allocated in the pipeline.

You simply create a PR branch to merge against master. Master should be thoroughly tested and when ready you would merge master into the production branch via PR as follows: 

```
Dev (any PR branch) -> Staging (master branch) -> Production (production branch)
```

#### Development Branches (PRs)
Any branch that is made a PR will be deployed to: https://knack-proxy-dev.austintexas.io/ This means that if you have multiple PRs, they will overwrite whatever is currently in that AWS function. Once you are happy with your PR (and test it thoroughly in Dev), you would merge your PR into the master branch.

#### Master Branch

The master branch is deployed automatically to the staging url: https://knack-proxy-staging.austintexas.io/ Once you are happy with the changes you ahve made, you should create a pull request against production.

#### Production Branch

The production branch is deployed automatically to the production url: https://knack-proxy.austintexas.io/

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
