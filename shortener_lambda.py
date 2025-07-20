import json
import boto3
import os
import random
import string

TABLE_NAME = os.environ.get("TABLE_NAME", "WhiskersURL")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # Handle CORS preflight request
    if event["requestContext"]["http"]["method"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps({"message": "CORS preflight success"})
        }

    try:
        body = json.loads(event.get("body", "{}"))
        long_url = body.get("url", "")

        if not long_url.startswith("http"):
            return respond(400, {"error": "Invalid URL"})

        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        table.put_item(Item={
            "id": short_id,
            "long_url": long_url
        })

        short_url = f"https://r6hbncei5lwdxlkkb5wyvo6fc40qrong.lambda-url.us-west-2.on.aws/{short_id}"
        return respond(200, {"shortUrl": short_url})

    except Exception as e:
        return respond(500, {"error": str(e)})

def respond(status, body):
    return {
        "statusCode": status,
        "headers": cors_headers(),
        "body": json.dumps(body)
    }

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }
