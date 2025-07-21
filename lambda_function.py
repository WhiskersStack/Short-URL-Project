import json
import boto3
import logging
import random
import string

TABLE_NAME = "WhiskersURL"   # hard-coded
BASE_URL = "https://mqdiderpf2effj7b7witmkoinm0zbkgk.lambda-url.us-west-2.on.aws"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    # ---- Logging to see what arrives ----
    logging.warning("EVENT=%s", json.dumps(event))

    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"].lstrip("/")      # ''  or 'AbC123'

    # === POST /  – create short link ==========================
    if method == "POST":
        body = json.loads(event.get("body", "{}"))
        long_url = body.get("url", "")
        if not long_url.startswith("http"):
            return _resp(400, {"error": "Invalid URL"})

        short_id = _gen_id()
        table.put_item(Item={"id": short_id, "long_url": long_url})

        return _resp(200, {"shortUrl": f"{BASE_URL}/{short_id}"})

    # === GET /{id} – redirect ================================
    if method == "GET" and path and path != "favicon.ico":
        item = table.get_item(Key={"id": path}).get("Item")
        if item:
            return {
                "statusCode": 302,
                "headers": {"Location": item["long_url"]},
                "body": ""
            }
        return _resp(404, {"error": "Not found"})

    # === fallback ============================================
    return _resp(405, {"error": "Method not allowed"})

# ---------- helpers -----------------------------------------


def _resp(code, body):
    return {
        "statusCode": code,
        "headers": {               # REMOVE CORS HEADERS HERE
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

# In the OPTIONS branch remove the CORS headers or delete the branch altogether


def _gen_id(n=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))
