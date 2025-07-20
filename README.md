# 🦊 Whiskers URL Shortener

A serverless URL shortener using AWS Lambda, DynamoDB, and S3.

![Architecture Diagram](https://mermaid.ink/img/pako\:eNp1Us1uwjAM_BXKYzdsQKWCRqFSaak2bYbGpQFHDMNGrChbNf79BzJgKka1L57p7Xv9t3WXlcLRRYa5CK0HhUdYJQBN6T5pj6AtcWYraDrb6Q6qChdJYILR-pSmZwVEXBqgp5jDtQ7-CmKRXTcFvffhqZ59AaQFhk9tOGTxwM1jsIuk55zOX8AqQpJ7npT4otsh5DrCgfHt06kXZv-Rj8VLD4pq_LTWd4Q4b-wzVN3PXmEYlQjGOF-fuM9u-2IjKGVYYPIlqsfF9u3Wc-fgDBcSghQ)

---

## 🚀 Features

* Shortens long URLs
* Stores mappings in DynamoDB
* Frontend hosted via S3
* Lambda Function URL backend

---

## 🛠️ How It Works

1. User submits a long URL from the public HTML form hosted on S3.
2. The form sends a POST request to the Lambda Function URL.
3. Lambda generates a short ID, stores the mapping in DynamoDB.
4. Returns a new shortened URL for the user.

---

## 📦 Setup

### 1. DynamoDB

* Table name: `WhiskersURL`
* Primary key: `id` (String)

### 2. S3 (Frontend)

* Upload `index.html`
* Make it public

### 3. Lambda (Backend)

* Python 3.12
* Use `main.py` and `helper.py`
* Add env var: `TABLE_NAME=WhiskersURL`
* Create Function URL (Auth: NONE)

### 4. Connect HTML

Update the form action in `index.html`:

```html
<form action="https://your-lambda-url.amazonaws.com/" method="POST">
```

---

## 🛡️ Security

* Enable CORS in Lambda
* Sanitize inputs
* For production: use API Gateway + IAM/Auth

---

## 🐾 Credits

Made with whiskers and love.

---

## 📄 License

MIT
