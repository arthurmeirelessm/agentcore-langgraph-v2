import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")


def get_embedding(text: str) -> list[float]:
    body = {
        "inputText": text
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["embedding"]
