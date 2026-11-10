   # Bedrock Hello

   A small Python script that sends a prompt to Amazon Bedrock (Nova Micro) and prints the reply.

   ## Run it
   python3 -m venv .venv
   source .venv/bin/activate
   pip install boto3
   python hello.py

   Needs AWS credentials configured (`aws configure`) and access to the model in us-east-1.

   ## What I learned
   - The Converse API uses the same call for different models
   - The parameter is `modelId`, and the SDK tells you when a name is wrong
