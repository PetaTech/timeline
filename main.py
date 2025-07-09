from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/health", response_class=JSONResponse)
def health_check():
    return {"status": "ok", "message": "Timeline server running"}


@app.get("/creed", response_class=HTMLResponse)
def render_creed_chart(request: Request):
    # Define timeline data
    df = pd.DataFrame([
        dict(Task="Day-of-Week Seasonality Module", Start='2025-07-10', Finish='2025-07-14', Budget="$80"),
        dict(Task="Mean-Reversion Engine (Déjà Vu)", Start='2025-07-15', Finish='2025-07-19', Budget="$120"),
        dict(Task="Regime Detection & Forecasting", Start='2025-07-20', Finish='2025-07-26', Budget="$150"),
        dict(Task="Portfolio Construction & Execution", Start='2025-07-27', Finish='2025-08-02', Budget="$170"),
        dict(Task="Monitoring & Reporting", Start='2025-08-03', Finish='2025-08-09', Budget="$130"),
    ])

    now = datetime.now()

    # Merge Budget into Task label
    df["Label"] = df["Task"] + " (" + df["Budget"] + ")"
    df["Color"] = df["Finish"].apply(lambda x: "green" if pd.to_datetime(x) < now else "#ff8311")

    # Build base figure with custom bar colors
    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[(pd.to_datetime(row["Finish"]) - pd.to_datetime(row["Start"])).days],
            y=[row["Label"]],
            base=pd.to_datetime(row["Start"]),
            orientation='h',
            marker=dict(color=row["Color"]),
            name=row["Label"],
            hovertemplate=f"Task: {row['Task']}<br>Start: {row['Start']}<br>End: {row['Finish']}<br>Budget: {row['Budget']}<extra></extra>"
        ))

    # Add vertical line at current datetime
    fig.add_vline(
        x=now,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text="Now",
        annotation_position="top right"
    )

    fig.update_layout(
        title="CREED Timeline: Renaissance-Inspired Strategy",
        barmode='stack',
        xaxis=dict(type='date', title="Date"),
        yaxis=dict(title="Milestone"),
        height=500,
        showlegend=False,
    )

    chart_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
    return templates.TemplateResponse("chart.html", {"request": request, "chart": chart_html})