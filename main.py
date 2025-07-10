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

    # Convert date strings to datetime objects
    df["Start_dt"] = pd.to_datetime(df["Start"])
    df["Finish_dt"] = pd.to_datetime(df["Finish"])
    
    # Calculate duration in days
    df["Duration"] = (df["Finish_dt"] - df["Start_dt"]).dt.days + 1  # +1 to include end date
    
    # Merge Budget into Task label
    df["Label"] = df["Task"] + " "
    df["Color"] = df["Finish_dt"].apply(lambda x: "green" if x < now else "#ff8311")

    # Build Gantt chart using plotly express (simpler approach)
    fig = px.timeline(
        df,
        x_start="Start_dt",
        x_end="Finish_dt",
        y="Label",
        color="Color",
        color_discrete_map={"green": "green", "#ff8311": "#ff8311"},
        title="CREED Timeline: Renaissance-Inspired Strategy"
    )
    
    # Update traces for better hover information
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                      "Start: %{x}<br>" +
                      "End: %{customdata[0]}<br>" +
                      "Duration: %{customdata[1]} days<br>" +
                      "Budget: %{customdata[2]}<br>" +
                      "<extra></extra>",
        customdata=df[["Finish", "Duration", "Budget"]].values
    )

    # Add vertical line at current datetime using add_shape instead of add_vline
    fig.add_shape(
        type="line",
        x0=now,
        x1=now,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(
            color="red",
            width=2,
            dash="dash"
        )
    )
    
    # Add annotation for "Now" label
    fig.add_annotation(
        x=now,
        y=1,
        yref="paper",
        text="Now",
        showarrow=False,
        xanchor="right",
        yanchor="bottom"
    )

    fig.update_layout(
        xaxis=dict(title="Date"),
        yaxis=dict(title="Milestone"),
        height=500,
        showlegend=False,
    )

    chart_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
    return templates.TemplateResponse("chart.html", {"request": request, "chart": chart_html})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)