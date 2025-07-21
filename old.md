# 🦊 Whiskers URL Shortener

A fully serverless URL shortener built with AWS Lambda, DynamoDB, and S3.

<img width="1024" height="1024" alt="whiskersstack-logo" src="https://github.com/user-attachments/assets/8962d43f-77f4-4844-8ffa-f9774cf760bb" />

---

## 📊 Architecture Overview

This diagram shows how the Whiskers URL Shortener system works from user submission to URL redirection. 🧭🔧🖥️

```
[User (Browser)]
     |
     v
[S3 Bucket: index.html Form] --POST--> [Lambda Function URL]
                                     |
                                     v
               [DynamoDB Table: WhiskersURL (short_id -> long_url)]
                                     |
                              [Returns JSON: short_url]
                                     |
                                     v
     (User receives short URL and clicks it later)
                                     |
                                     v
       [API Gateway: /{short_id}] --> [Redirect Lambda]
                                     |
                                     v
               [DynamoDB Table: WhiskersURL]
                                     |
                              [HTTP Redirect to long_url]
```

---

## 🚀 Features

* Shortens long URLs in seconds
* Stores short ID mappings in DynamoDB
* Static frontend hosted on Amazon S3
* Backend logic handled by AWS Lambda and exposed via Function URL

---

## 🛠️ How It Works

1. The user opens the static HTML form hosted on an S3 bucket.
2. They submit a long URL via the form.
3. The Lambda function receives the POST request, generates a short ID, and stores it with the original URL in DynamoDB.
4. The user receives a shortened URL in response.

---

## 📦 Setup Guide

### 1. DynamoDB

* Go to **DynamoDB** → **Create Table**
* Set:

  * Table name: `WhiskersURL`
  * Partition key: `id` (String)

<img width="987" height="492" alt="Screenshot 2025-07-20 193529" src="https://github.com/user-attachments/assets/38160172-3b04-4d27-a06c-476cf935b5e6" />

### 2. S3 (Static Website Hosting)

* Create a bucket named e.g. `whiskers-url-shortener`
* Enable ACLs
* Disable **"Block all public access"**
* Upload your `index.html` file
* Make the file publicly accessible

<img width="1650" height="432" alt="Screenshot 2025-07-20 193916" src="https://github.com/user-attachments/assets/dcb75fcd-0d46-44d2-b256-85a5dae95db0" />
<img width="1641" height="502" alt="Screenshot 2025-07-20 193924" src="https://github.com/user-attachments/assets/b2dae261-3cee-46b5-9c85-c15ff3dc4c4f" />
<img width="596" height="474" alt="Screenshot 2025-07-20 194014" src="https://github.com/user-attachments/assets/9ab47c28-feac-4f35-bf27-8eba0740ff11" />


### 3. Lambda (Backend API)

* Create a Lambda function

  * Runtime: **Python 3.12**
  * Use an existing role with **LabRole**
  * Enable the **Function URL**
  * Set **Auth type** to `NONE`
  * Copy the URL (e.g. `https://xyz.lambda-url.us-east-1.on.aws/`)

<img width="1203" height="286" alt="Screenshot 2025-07-20 195246" src="https://github.com/user-attachments/assets/33b12b78-94b0-4e50-8797-1f962f6af00e" />
<img width="1489" height="960" alt="Screenshot 2025-07-20 193754" src="https://github.com/user-attachments/assets/0fb909d3-a154-4ce0-8ade-7d82183b04a5" />
<img width="520" height="65" alt="image" src="https://github.com/user-attachments/assets/52afe329-1fc4-458b-97e6-2d7698946f85" />


### 5. HTML Form Integration

Update your HTML form tag like so:

```html
<form action="https://your-lambda-url.amazonaws.com/" method="POST">
```

---

## 🐍 Lambda Code

<img width="347" height="261" alt="image" src="https://github.com/user-attachments/assets/5a793d14-c80c-41ea-b4a3-d18ed90db3d3" />

### `lambda_function.py`

```python
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

# Rest of the script...
```

### `WhiskersRedirect.py`

```python
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

# Rest of the script...
```

---

## 🔐 Security Best Practices

* Enable CORS in your Lambda function to allow browser requests
* Sanitize and validate all user input to prevent injection attacks
* Use **API Gateway + IAM authentication** for more control in production environments

---

<img width="540" height="410" alt="image" src="https://github.com/user-attachments/assets/4a1a6b38-9ba9-459a-877f-f69f1becf503" />

