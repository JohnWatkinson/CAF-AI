🧠 About site_pages.schema.json
This JSON Schema defines the expected structure for any site_pages/*.json file used in the CAF-AI knowledge ingestion system.

It ensures that:

All required fields are present (like topic, region, brand, etc.)

Each page entry contains the necessary information (url, title, text, retrieved_at)

Dates are correctly formatted

The structure is predictable, safe to ingest, and easy to debug

✅ Why Use This Schema?
Using a schema lets you:

Validate scraper output before ingestion

Fail fast if a field is missing or broken

Prevent silent data issues that break your AI system downstream

Standardize collaboration if others contribute data

📁 Example Valid site_pages/*.json
json
Copy
Edit
{
  "description": "Scraped IMU content from Torino website",
  "base_url": "https://www.comune.torino.it/imu",
  "topic": "imu",
  "region": "torino",
  "brand": "CAF",
  "pages": [
    {
      "url": "https://www.comune.torino.it/imu/faq",
      "title": "Domande frequenti sull'IMU",
      "text": "Il contribuente che riceve un avviso di accertamento...",
      "retrieved_at": "2024-02-23"
    }
  ]
}
🔒 Key Rules Enforced
Field	Type	Notes
topic	string	Required — e.g. imu, f24, tari
region	string	Required — e.g. torino, milano
brand	string	Required — CAF, MG, etc.
retrieved_at	string	Must be ISO YYYY-MM-DD format
text	string	Must be 20+ characters long
