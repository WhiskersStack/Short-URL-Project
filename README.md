# 🐱‍💻 WhiskersStack URL Shortener

Paste a long link, click **Shorten**, and get a tidy cat‑powered URL back! 😸🔗
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/e53fec5c-ae85-4d1b-acea-3333c4e4f518" />

---

## 🚀 Features

* **Serverless & Lightweight** – zero infrastructure to patch or babysit.
* **Custom Short IDs** – six‑character alphanumerics generated on the fly.
* **One‑click Copy** – quick share button (coming soon!).
* **DynamoDB Analytics‑Ready** – every redirect can be counted for stats.
* **Full Dark Mode** – purr‑fect for night owls.

---

## 🏗️ Architecture

| Layer        | AWS Service                             | Emoji |
| ------------ | --------------------------------------- | ----- |
| Frontend     | **S3 Static Website**                   | 🌐    |
| API Endpoint | **Lambda Function URL**                 | 🌀    |
| Compute      | **AWS Lambda (Python 3.13)**            | 🐍    |
| Data Store   | **DynamoDB** (PK=`id`)                  | 📊    |
| Permissions  | **IAM Role** with `GetItem` / `PutItem` | 🔐    |

*Everything is provisioned manually in the **AWS Console** — no Terraform, SAM, or CDK required.*

---

## 🛠️ Step‑by‑Step Setup (Console‑only)

1. ### **Create the DynamoDB Table**

   | Setting       | Value         |
   | ------------- | ------------- |
   | Table name    | `WhiskersURL` |
   | Partition key | `id` (String) |

2. ### **Deploy the Lambda Function**

   1. Runtime → **Python 3.13**.
   2. Upload `lambda_function.py` (see `/src` folder).
   3. Handler → `lambda_function.lambda_handler`.
   4. Memory → **128 MB** is fine; Timeout → **3 s**.
   5. **Execution role** → select existing role **LabRole** (or create one) and attach inline policy:

      ```json
      {
        "Effect": "Allow",
        "Action": ["dynamodb:GetItem","dynamodb:PutItem"],
        "Resource": "arn:aws:dynamodb:<REGION>:<ACCOUNT>:table/WhiskersURL"
      }
      ```

3. ### **Enable a Function URL**

   1. Auth type → **NONE**.
   2. CORS → Allow origin `*`, methods `GET,POST,OPTIONS`, headers `Content-Type`.
   3. Copy the generated URL – call it **`BASE_URL`**.

4. ### **Upload the Frontend to S3**

   1. Create an **S3 bucket** with **public‑read** (static hosting) enabled and **ACLs turned ON** (Bucket → Permissions → Object Ownership → Enable ACLs).
   2. Edit `WhiskersURL.html`: update the `fetch()` URL to your **`BASE_URL`**.
   3. Upload HTML + logo PNG.

5. ### **Test It!**

   1. Visit the S3 website endpoint.
   2. Paste a long link → **Shorten**.
   3. Click the returned short URL – you should see a 302 redirect to the original site.

---

## 🌈 Roadmap / Ideas

* 📈 **Click counters** (increment a `hits` attribute per redirect).
* ⏳ **TTL / Expiry** – auto‑delete stale links via DynamoDB TTL.
* 🔗 **Custom Domain** – map `whis.rs` via CloudFront & ACM.
* 📋 **Copy button & toast** – polished UX.

---

## 🤝 Contributing

Found a bug or have an epic idea? Open an issue or PR! Everyone’s welcome in the litter box.

---

## 📜 License

MIT – use it, remix it, just don’t blame the cat if you break it. 🐾
