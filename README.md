# Bedrock Hello

A Python application that sends a prompt to Amazon Bedrock using the Amazon Nova Micro model and prints the response.

This project explores how to build, containerize, and securely run a Python application using Docker and AWS credentials.

## Project Objectives

- Connect a Python application to Amazon Bedrock.
- Use the Amazon Bedrock Converse API.
- Package the application into a Docker image.
- Run the container as a non-root user.
- Understand how AWS credentials are accessed inside containers.
- Apply security practices when building and running Docker containers.

## Technologies Used

- Python 3.12
- Amazon Bedrock
- Amazon Nova Micro
- Boto3
- Docker
- Git and GitHub
- Ubuntu on WSL

## Running Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install boto3
```

Configure AWS credentials using an appropriate AWS credential provider, then run:

```bash
python hello.py
```

The application requires access to Amazon Bedrock and permission to invoke the selected model in the configured AWS region.

## Building the Docker Image

Build the image:

```bash
docker build -t bedrock-hello .
```

Run the container:

```bash
docker run --rm bedrock-hello
```

The application uses AWS credentials supplied at runtime.

## Docker Security: Running as a Non-Root User

Initially, the container ran as the root user.

I updated the Dockerfile to:

- Create a dedicated Linux user called `appuser`.
- Copy the application into the image with the correct ownership.
- Switch to `appuser` using the Docker `USER` instruction.

This ensures that the application does not run as root inside the container.

To verify the configured user:

```bash
docker image inspect bedrock-hello --format '{{.Config.User}}'
```

To inspect the container's user identity:

```bash
docker run --rm --entrypoint id bedrock-hello
```

The output confirmed that the application runs as UID 1000 (`appuser`).

## AWS Credentials Inside Docker

After switching to a non-root user, the application initially failed with a `NoCredentialsError`.

The problem was not the Python application or Docker image. The AWS credentials were stored in files owned by root with restrictive permissions, so the non-root container user could not read them.

For this demonstration, I tested a temporary credential-copy approach:

1. Copied the AWS configuration and credentials into a temporary directory.
2. Changed ownership of the temporary copies to UID 1000.
3. Restricted directory permissions.
4. Mounted the directory into the container as read-only.
5. Ran the application successfully.
6. Removed the temporary credential directory.

This helped demonstrate how Linux file ownership and permissions affect access inside containers.

**Important:** This was a learning workaround, not a recommended production credential-management strategy. In production, use IAM roles, workload identity, or another secure AWS credential provider rather than copying long-lived credentials.

## Security Practices

The project uses `.gitignore` and `.dockerignore` to exclude sensitive or unnecessary files, including:

- `.aws/`
- `.env` files
- Credential files
- Private keys
- Python virtual environments
- Git metadata

AWS credentials and secrets should never be copied into a Docker image or committed to a public GitHub repository.

## What

## What I Learned

- How to call Amazon Bedrock using Boto3 and the Converse API.
- How to build and run a Docker image.
- Why containers should run as non-root users.
- How Linux ownership and file permissions affect container access.
- Why a container may fail to access AWS credentials even when they work on the host.
- Why credentials should be supplied securely at runtime.
- How `.gitignore` and `.dockerignore` help protect sensitive files.

## Future Improvements

- Use IAM roles or another secure credential provider for container execution.
- Add automated tests.
- Add a CI/CD workflow using GitHub Actions.
- Explore deploying the application to AWS.

## Author

Bobo-ops01
