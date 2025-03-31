import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import requests
import json
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Healthcare Inbox Triage Dashboard", className="text-center my-4")
        ])
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filters", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Date Range"),
                            dcc.DatePickerRange(
                                id='date-range',
                                start_date=datetime.now() - timedelta(days=7),
                                end_date=datetime.now(),
                                display_format='YYYY-MM-DD'
                            )
                        ]),
                        dbc.Col([
                            html.Label("Triage Category"),
                            dcc.Dropdown(
                                id='category-filter',
                                options=[
                                    {'label': 'All', 'value': 'ALL'},
                                    {'label': 'Critical', 'value': 'CRITICAL'},
                                    {'label': 'High', 'value': 'HIGH'},
                                    {'label': 'Medium', 'value': 'MEDIUM'},
                                    {'label': 'Low', 'value': 'LOW'},
                                    {'label': 'Reference', 'value': 'REFERENCE'}
                                ],
                                value='ALL'
                            )
                        ])
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Statistics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Messages", className="card-title"),
                    html.H2(id="total-messages", className="text-center")
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Critical Messages", className="card-title"),
                    html.H2(id="critical-count", className="text-center text-danger")
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("High Priority", className="card-title"),
                    html.H2(id="high-count", className="text-center text-warning")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Messages by Category", className="card-title"),
                    dcc.Graph(id="category-pie")
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Messages Over Time", className="card-title"),
                    dcc.Graph(id="time-series")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Message List
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Messages", className="card-title"),
                    html.Div(id="message-list")
                ])
            ])
        ])
    ])
], fluid=True)

def get_messages(category=None, start_date=None, end_date=None):
    """Fetch messages from the API with optional filters."""
    params = {}
    if category and category != 'ALL':
        params['category'] = category
    if start_date:
        params['start_date'] = start_date.isoformat()
    if end_date:
        params['end_date'] = end_date.isoformat()
        
    response = requests.get('http://localhost:8000/messages', params=params)
    return response.json()

def get_stats():
    """Fetch statistics from the API."""
    response = requests.get('http://localhost:8000/stats')
    return response.json()

@app.callback(
    [Output("total-messages", "children"),
     Output("critical-count", "children"),
     Output("high-count", "children"),
     Output("category-pie", "figure"),
     Output("time-series", "figure"),
     Output("message-list", "children")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("category-filter", "value")]
)
def update_dashboard(start_date, end_date, category):
    # Convert date strings to datetime objects
    if start_date:
        try:
            # Try parsing as ISO format first
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except ValueError:
            # Fallback to YYYY-MM-DD format
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if end_date:
        try:
            # Try parsing as ISO format first
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            # Fallback to YYYY-MM-DD format
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Fetch data
    messages = get_messages(category, start_date, end_date)
    stats = get_stats()
    
    # Update statistics
    total = stats['total_messages']
    critical = stats['categories'].get('CRITICAL', 0)
    high = stats['categories'].get('HIGH', 0)
    
    # Create pie chart
    pie_fig = px.pie(
        values=list(stats['categories'].values()),
        names=list(stats['categories'].keys()),
        title="Messages by Category"
    )
    
    # Create time series
    df = pd.DataFrame(messages)
    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Resample to daily counts and fill missing values with 0
        daily_counts = df.groupby(['datetime', 'triage_category']).size().unstack(fill_value=0)
        daily_counts = daily_counts.resample('D').sum().fillna(0)
        
        time_fig = px.line(
            daily_counts,
            title="Messages Over Time",
            labels={
                'datetime': 'Date',
                'value': 'Number of Messages',
                'triage_category': 'Category'
            }
        )
        
        # Update layout for better readability
        time_fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Messages",
            hovermode='x unified'
        )
    else:
        time_fig = go.Figure()
        time_fig.update_layout(
            title="No messages in selected time period",
            showlegend=False
        )
    
    # Create message list
    message_cards = []
    for msg in messages:
        color = {
            'CRITICAL': 'danger',
            'HIGH': 'warning',
            'MEDIUM': 'info',
            'LOW': 'success',
            'REFERENCE': 'secondary'
        }.get(msg['triage_category'], 'light')
        
        message_cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.H5(msg['subject'], className="card-title"),
                    html.P(msg['content'], className="card-text"),
                    dbc.Badge(msg['triage_category'], color=color, className="me-2"),
                    dbc.Button("Mark as Read", color="primary", size="sm", className="me-2"),
                    dbc.Button("Reclassify", color="secondary", size="sm")
                ])
            ], className="mb-3")
        )
    
    return total, critical, high, pie_fig, time_fig, message_cards

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.getenv('DASH_HOST', '127.0.0.1')
    port = int(os.getenv('DASH_PORT', '8050'))
    
    app.run(debug=True, host=host, port=port) 