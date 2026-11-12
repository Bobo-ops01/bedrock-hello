# Bedrock Hello – Python, Amazon Bedrock and Docker

A small Python application that sends a prompt to Amazon Bedrock using the Converse API and prints the response from Amazon Nova Micro.

This project explores Python, AWS SDK integration, Docker containerisation and container security.

## Project objectives

- Connect a Python application to Amazon Bedrock using boto3.
- Use the Bedrock Converse API to send prompts and receive responses.
- Containerise the application using Docker.
- Apply the principle of least privilege by running the container as a non-root user.
- Handle AWS credentials securely without baking them into the Docker image.

## Technologies used

- Python 3.12
- Amazon Bedrock (Nova Micro)
- AWS SDK for Python (boto3)
- Docker
- Linux

## Running locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install boto3
```

Configure AWS credentials and ensure your account has access to the selected Bedrock model in `us-east-1`.

Run the application:

```bash
python hello.py
```

## Running with Docker

Build the Docker image:

```bash
docker build -t bedrock-hello .
```

The Dockerfile:
- Uses the Python 3.12 slim image.
- Installs boto3.
- Creates a dedicated Linux user called `appuser`.
- Assigns ownership of the application script to `appuser`.
- Uses `USER appuser` to run the application without root privileges.

Verify the configured user:

```bash
docker image inspect bedrock-hello --format '{{.Config.User}}'
```

Expected output:

```text
appuser
```

## AWS credentials and container security

Initially, the container could not locate AWS credentials.

After switching from root to `appuser`, another issue appeared: the mounted AWS credential files were owned by root and had restrictive `600` permissions.

The non-root user could not read them.

Rather than making the credentials world-readable, I created a temporary copy, assigned it to the container user's UID and mounted it read-only.

Example:

```bash
aws_tmp=$(mktemp -d)
trap 'rm -rf "$aws_tmp"' EXIT

cp -a ~/.aws/. "$aws_tmp/"
chown -R 1000:1000 "$aws_tmp"
chmod 700 "$aws_tmp"

docker run --rm \
  -v "$aws_tmp:/home/appuser/.aws:ro" \
  bedrock-hello
```

The application successfully called Amazon Bedrock while running as `appuser`.

The temporary credentials directory was removed after testing.

**Security note:** AWS credentials should never be copied into a Docker image or committed to GitHub. For production workloads, prefer an appropriate IAM role or secure workload credential provider rather than copying long-lived credentials.

## Security practices applied

- Run containers as non-root users.
- Apply the principle of least privilege.
- Mount credentials read-only when required.
- Exclude sensitive files using `.gitignore` and `.dockerignore`.
- Avoid embedding AWS credentials in Docker images.

## What I learned

- The Bedrock Converse API provides a consistent interface for interacting with supported models.
- The API parameter is `modelId`.
- boto3 reports errors when an invalid model identifier is supplied.
- Docker images package applications and their runtime dependencies.
- Changing the Docker user affects access to mounted files.
- Linux file ownership and permissions matter inside containers.
- Security improvements can introduce new access issues that need to be investigated and tested.

## Project structure

```text
bedrock-hello/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── hello.py
├── README.md
└── notes.txt
```

## Future improvements

- Add automated Docker builds using GitHub Actions.
- Improve image size and dependency management.
- Explore IAM roles and more secure AWS credential delivery.
- Add automated tests.

This is a hands-on learning project documenting my journey with AWS, Python, Docker and cloud security.
