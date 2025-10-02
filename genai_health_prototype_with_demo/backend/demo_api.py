
"""Demo FastAPI app: demo_api.py
- Serves summary at /summary
- Serves chart images at /charts/<name>.png
- Simple rule-based insights at /insights
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd, os, io, datetime
import matplotlib.pyplot as plt

APP_DIR = os.path.dirname(__file__)
DATA_CSV = os.path.join(APP_DIR, '..', 'input_data', 'diabetes.csv')
CHARTS_DIR = os.path.join(APP_DIR, 'static_charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

app = FastAPI(title='GenAI Chronic Care - Demo API')

def load_data():
    df = pd.read_csv(DATA_CSV)
    return df

def make_charts():
    df = load_data()
    charts = {}
    try:
        # 1) Glucose distribution if present
        if 'glucose_mg_dl' in df.columns:
            plt.figure()
            df['glucose_mg_dl'].dropna().hist(bins=30)
            p = os.path.join(CHARTS_DIR, 'glucose_hist.png')
            plt.title('Glucose Distribution')
            plt.xlabel('mg/dL')
            plt.ylabel('Count')
            plt.savefig(p)
            plt.close()
            charts['glucose_hist'] = p
    except Exception as e:
        print('Glucose chart error:', e)
    try:
        # 2) Heart rate trend if present (first 200 rows)
        if 'heart_rate' in df.columns:
            plt.figure()
            df['heart_rate'].dropna().head(200).reset_index(drop=True).plot()
            p = os.path.join(CHARTS_DIR, 'heart_rate_trend.png')
            plt.title('Heart Rate Trend (first 200 records)')
            plt.xlabel('Record index')
            plt.ylabel('BPM')
            plt.savefig(p)
            plt.close()
            charts['heart_rate_trend'] = p
    except Exception as e:
        print('Heart rate chart error:', e)
    try:
        # 3) Blood pressure scatter if systolic/diastolic present
        if 'systolic_bp' in df.columns and 'diastolic_bp' in df.columns:
            plt.figure()
            plt.scatter(df['systolic_bp'].dropna(), df['diastolic_bp'].dropna(), s=10)
            p = os.path.join(CHARTS_DIR, 'bp_scatter.png')
            plt.title('Systolic vs Diastolic BP')
            plt.xlabel('Systolic')
            plt.ylabel('Diastolic')
            plt.savefig(p)
            plt.close()
            charts['bp_scatter'] = p
    except Exception as e:
        print('BP chart error:', e)
    return charts

def summarize():
    df = load_data()
    summary = {
        'rows': int(df.shape[0]),
        'columns': df.columns.tolist(),
        'generated_at': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    # simple statistics for numeric cols, limited set
    num = df.select_dtypes(include='number').describe().to_dict()
    summary['numeric_stats'] = num
    # Simple rule-based flags: count of high glucose >180, hr>100
    flags = {}
    if 'glucose_mg_dl' in df.columns:
        flags['high_glucose_count'] = int((df['glucose_mg_dl']>180).sum())
    if 'heart_rate' in df.columns:
        flags['tachy_count'] = int((df['heart_rate']>100).sum())
    if 'systolic_bp' in df.columns and 'diastolic_bp' in df.columns:
        flags['hypertensive_count'] = int(((df['systolic_bp']>140)|(df['diastolic_bp']>90)).sum())
    summary['flags'] = flags
    return summary

# Pre-generate charts on startup
CHARTS = make_charts()
SUMMARY = summarize()

@app.get('/summary')
def get_summary():
    return JSONResponse(SUMMARY)

@app.get('/insights')
def get_insights():
    # Return simple rule-based insights for demo purposes
    df = load_data()
    insights = []
    if 'glucose_mg_dl' in df.columns and (df['glucose_mg_dl']>180).any():
        insights.append('Some readings indicate high blood glucose (>180 mg/dL). Follow diabetes action plan.')
    if 'heart_rate' in df.columns and (df['heart_rate']>100).any():
        insights.append('Some readings show elevated heart rate (>100 bpm). Consider evaluation.')
    if 'systolic_bp' in df.columns and 'diastolic_bp' in df.columns and (((df['systolic_bp']>140)|(df['diastolic_bp']>90)).any()):
        insights.append('Some blood pressure readings are in hypertensive range. Recheck and consult.')
    return JSONResponse({'insights': insights})

@app.get('/charts/{name}.png')
def get_chart(name: str):
    # serve chart file if present
    key = name + '.png'
    for v in CHARTS.values():
        if v.endswith(key):
            return FileResponse(v, media_type='image/png')
    raise HTTPException(status_code=404, detail='Chart not found')
