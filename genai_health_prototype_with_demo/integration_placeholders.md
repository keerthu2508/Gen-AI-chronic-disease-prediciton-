Integration placeholders (limit: 2 external APIs)

1) Wearable API (example)
   - Purpose: ingest step count, heart rate, SpO2, sleep, active minutes.
   - Flow: OAuth2 -> subscribe to user's device -> webhook for real-time pushes -> batch sync

   Example endpoints (placeholder):
   - POST /oauth/token  (get access token)
   - GET /user/devices
   - GET /devices/{id}/metrics?from=...&to=...
   - Webhook: POST /webhook/wearable

   Security: use TLS, validate webhooks, map device IDs to patient_id in DB.

2) Pharmacy API (example)
   - Purpose: lookup medicines, send prescriptions, check local pharmacy stock, place orders.
   - Flow: API key or OAuth, send prescription payload, receive order confirmation.

   Example endpoints (placeholder):
   - POST /pharmacy/prescriptions
   - GET /pharmacy/stock?medicine=...

Keep integrations to two external services to match your restriction.
