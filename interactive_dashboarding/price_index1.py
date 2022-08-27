from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Master Data.csv")

df.Date = pd.to_datetime(df.Date)
app = Dash()

city_dropdown = dcc.Dropdown(options=df['City'].unique(),
                             value=['Average','Karachi'],
                             multi=True,
                             id='city_dropdown_id')

product_dropdown = dcc.Dropdown(options=df['Description'].unique(),
                                value=['Wheat','Wheat Flour Bag'],
                                multi=True,
                                id='product_dropdown_id')

year_slider = dcc.RangeSlider(df['Year'].min(),
                              df['Year'].max(),
                              step=1,
                              value=[df['Year'].min(),
                                     df['Year'].max()],
                              tooltip={"placement": "bottom", "always_visible": True},
                              id='year_slider_id',
                              marks={str(year): str(year) for year in df['Year'].unique()})

app.layout = html.Div(children=[
    html.H1(children='Commodity Price Index'),
    city_dropdown,
    product_dropdown,
    dcc.Graph(id='commodity_price_index',
              config={'displayModeBar': False #This config command is to hide the plotly toolbar.
                     }
             ),
    year_slider,
])

@app.callback(
    Output(component_id='commodity_price_index',component_property='figure'),
    Input(component_id='city_dropdown_id',component_property='value'),
    Input(component_id='product_dropdown_id',component_property='value'),
    Input(component_id='year_slider_id',component_property='value')
)

def update_graph(city_fig,product_fig,year_fig):
    dff = df[(df['Year'].isin(year_fig)) & (df['City'].isin(city_fig)) & (df['Description'].isin(product_fig))]
    line_fig = px.line(dff,
                       x='Date',
                       y='Price',
                       color='City',
                       line_dash = 'Description',
                       title=f'Government Issued Price Index for {product_fig} in {city_fig}')
    
    
    line_fig.update_xaxes(title='Year')
    
    line_fig.update_yaxes(title='Price')
    
# Following lines can be added if we want to create a input page separately and view the chart.
#     line_fig.show(config=dict(displayModeBar=False)
#     )
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)