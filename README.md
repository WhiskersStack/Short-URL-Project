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

<img width="978" height="407" alt="image" src="https://github.com/user-attachments/assets/2540629c-3da8-4086-a065-4e400cd80fa4" />

2. ### **Deploy the Lambda Function**

   1. Runtime → **Python 3.13**.
   2. **Execution role** → select existing role **LabRole**.
   3. Enbale **Function URL** + Auth type = **NONE**.
   4. Upload `lambda_function.py` (see `/src` folder).

<img width="380" height="242" alt="image" src="https://github.com/user-attachments/assets/8ff31cfd-955f-4c3b-9f44-628488b389ea" />
<img width="368" height="267" alt="image" src="https://github.com/user-attachments/assets/8217fcc0-9435-428c-8cec-74a9407efa9e" />
<img width="498" height="427" alt="image" src="https://github.com/user-attachments/assets/373b5fea-695b-4223-9f09-b2f622caccf7" />


3. ### **Configure Function URL**

   1. CORS → Allow origin `*`, methods `*`, headers `Content-Type`.
   2. Copy the generated URL, into the **Lambda** – call it **`BASE_URL`**.
      
<img width="387" height="683" alt="image" src="https://github.com/user-attachments/assets/53f16437-95b4-471b-9526-dc59efb1e5fb" />
<img width="481" height="87" alt="image" src="https://github.com/user-attachments/assets/f2903cef-0896-457a-ba65-e779d8fd0965" />

4. ### **Upload the Frontend to S3**

   1. Create an **S3 bucket** with **public‑read** (static hosting) enabled and **ACLs turned ON**.
   2. Edit `WhiskersURL.html`: update the `fetch()` URL to your **`BASE_URL`**.
   3. Upload HTML + logo PNG, and **Make them public by using ACLs**.
      
<img width="951" height="334" alt="image" src="https://github.com/user-attachments/assets/1946b83f-9273-4ad8-a955-da06178dc6eb" />
<img width="524" height="469" alt="image" src="https://github.com/user-attachments/assets/7b6e738e-036c-4598-ba29-83ef17b93c6e" />
<img width="254" height="482" alt="image" src="https://github.com/user-attachments/assets/781264d2-13fe-42f2-8293-69c473f6d646" />

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
