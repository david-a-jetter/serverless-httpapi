import boto3

client = boto3.client("secretsmanager")


def get_secret_value(environment: str, suffix: str) -> str:
    secret_id = f"{environment}-{suffix}"
    secret = client.get_secret_value(secret_id)
    return secret["SecretString"]
