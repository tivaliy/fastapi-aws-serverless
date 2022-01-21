# fastapi-aws-serverless

FastAPI + Amazon API Gateway + Lambda - simple demo application


## Prerequisites

- AWS Account
- AWS Command Line Tool (CLI) - `aws` [aws cli installation guide]
- AWS Serverless Application Model (SAM) with a command line tool AWS SAM CLI - `sam` [sam cli installation guide]


## Getting Up and Running Locally with Docker

Open a terminal at the project root and run the following for local development:

  - Build the Stack:

          $ docker-compose build

  - Run the Stack (use `-d` to run in the detached mode):

          $ docker-compose up

  - Run the stack in Debugging mode (with *ipdb* support):

          $ docker-compose run --rm --service-ports backend

By default, service will be available on the following routes:

    http://0.0.0.0:8888/docs
    http://0.0.0.0:8888/redoc
    http://0.0.0.0:8888/openapi.json


  [installation instructions]: https://docs.docker.com/install/#supported-platforms
  [installation guide]: https://docs.docker.com/compose/install/

## Run tests

Create isolated Python environment `virtualenv venv` and activate it `source venv/bin/activate`

Install all necessary dependencies: `pip install -r test-requirements.txt`

Run tests:

    pytest tests -v  # increase verbosity

with coverage report:

    pytest --cov=app tests


## Build the Stack

For building the stack run:

    sam build -t template.yaml


## Deploy the Stack

For deploying appropriate Stack (`dev`, `prod`) run (with guided prompts):

    sam deploy --guided --capabilities CAPABILITY_IAM --config-env dev|prod


For newly created API Gateway endpoint URL see CloudFormation outputs, ex.:

    CloudFormation outputs from deployed stack
    ------------------------------------------------------------------------------------------
    Outputs
    -----------------------------------------------------------------------------------------
    Key                 FastAPI
    Description         API Gateway endpoint URL
    Value               https://abcdefgh12.execute-api.us-east-1.amazonaws.com/dev
    -----------------------------------------------------------------------------------------

Service will be available on the following routes:

    https://abcdefgh12.execute-api.us-east-1.amazonaws.com/dev/docs
    https://abcdefgh12.execute-api.us-east-1.amazonaws.com/dev/redoc
    https://abcdefgh12.execute-api.us-east-1.amazonaws.com/dev/openapi.json



## Delete the Stack

For deleting the Stack run:

    sam delete --stack-name your-stack-name


  [aws cli installation guide]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
  [sam cli installation guide]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
