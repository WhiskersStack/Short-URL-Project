import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("TABLE_NAME", "WhiskersURL")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    raw_path = event.get("rawPath", "/")
    short_id = raw_path.lstrip("/")

    if not short_id:
        return error_page(400, "Missing short code")

    response = table.get_item(Key={"id": short_id})
    item = response.get("Item")

    if not item:
        return error_page(404, "Link not found")

    return {
        "statusCode": 302,
        "headers": {
            "Location": item["long_url"]
        },
        "body": ""
    }

def error_page(status, message):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "text/html"},
        "body": f"<h2>{message}</h2>"
    }
