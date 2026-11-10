import boto3

MODEL_ID = "amazon.nova-micro-v1:0"

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": [{"text": "Explain Infrastructure as Code in two sentences."}],
        }
    ],
    inferenceConfig={"maxTokens": 200},
)

print(response["output"]["message"]["content"][0]["text"])
