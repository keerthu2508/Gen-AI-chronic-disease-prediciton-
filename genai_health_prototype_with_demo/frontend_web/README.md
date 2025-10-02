
Demo run instructions
---------------------
1) Backend (FastAPI)
   - Ensure Python requirements: fastapi, uvicorn, pandas, matplotlib
   - From the 'backend' directory, run:
       uvicorn demo_api:app --reload --host 0.0.0.0 --port 8000
   - The API serves:
       GET /summary  -> JSON summary
       GET /insights -> JSON insights
       GET /charts/<name>.png  -> chart images (glucose_hist, heart_rate_trend, bp_scatter)

2) Frontend (static)
   - Serve frontend_web/index.html from the same origin as backend (or use a simple static server)
   - Example (from WORKDIR):
       python -m http.server 8080  # then open http://localhost:8080/frontend_web/index.html
   - If backend runs on port 8000 and frontend on 8080, update fetch URLs in index.html to point to http://localhost:8000/summary etc.
