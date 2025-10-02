# GenAI Chronic Care - Prototype Scaffold

    This scaffold contains:
    - backend/: Python data processing and FastAPI skeleton
    - frontend/: React Native starter App.js and notes for offline reminders
    - db/: PostgreSQL schema with example pgcrypto usage for encrypted fields
    - integration_placeholders.md: details on two external API integrations
    - input_data/: extracted files from your uploaded ZIP (if any)

    ## Tools / Stack (as requested)
    - OpenAI GPT-4 or Google Gemini (hooks only — you must supply API keys) for health recommendations.
    - Python (pandas, scikit-learn) for data analysis (see backend/data_processing.py).
    - React Native for mobile application (see frontend/App.js).
    - PostgreSQL with pgcrypto for encryption of sensitive fields (see db/schema.sql).
    - Limit external integrations to a maximum of 2 (example placeholders provided).

    ## Offline capability
    - Medication reminders are stored in local device storage (AsyncStorage) to work offline.
    - For critical alerts, the app should queue messages and sync when connectivity resumes.

    ## Response time constraint
    - The backend analyze endpoint is lightweight and uses rule-based logic to ensure fast responses (<30s).
    - Heavy ML model inference should be optimized or run asynchronously with progress updates.

    ## How to run
    1. Backend:
       - Create virtualenv, install requirements (fastapi, uvicorn, pandas, scikit-learn, joblib).
       - Run: `python backend/api.py`
    2. Frontend:
       - Initialize a React Native project and replace App.js with frontend/App.js.
       - Install AsyncStorage and run on device/emulator.
    3. Database:
       - Run SQL in db/schema.sql on PostgreSQL with pgcrypto enabled.

    ## Files extracted from your uploaded ZIP
    [
  "diabetes.csv"
]


## Demo API & Web UI
Added `backend/demo_api.py` and `frontend_web/index.html` for a simple demo dashboard that loads the provided diabetes.csv and serves charts and insights.
