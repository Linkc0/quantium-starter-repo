import pandas
from dash import Dash, Input, Output, html, dcc
from plotly.express import line

DATA_PATH = "./formatted_data.csv"
COLORS = {
    "primary": "#98A7E4",
    "secondary": "#555065",
    "font": "#000000"
}

data = pandas.read_csv(DATA_PATH)
data = data.sort_values(by="date")

app = Dash(__name__)

def chartGeneration(data):
    chart = line(data, x="date",y="sales",title="Pink Morsel Sales")
    chart.update_layout(
        title_font_color=COLORS["secondary"],
        title_font_size=24,
        xaxis_title="Date",
        yaxis_title="Sales",
        font_color=COLORS["font"]
    )
    return chart


visualization = dcc.Graph(
        id="visualization",
        figure=chartGeneration(data)
    )
  


title = html.H1(
    "Visualizer for Pink Morsel Sales",
    id="title",
    style=(
        {
            "color": COLORS["font"],
            "textAlign": "center",
            "marginBottom": "20px"
        }
    )
)

regionPicker= dcc.Dropdown(
    id="region-picker",
    options=[
        {"label": "All Regions", "value": "all"},
        {"label": "North", "value": "north"},
        {"label": "South", "value": "south"},
        {"label": "East", "value": "east"},
        {"label": "West", "value": "west"}
    ],
    value="all",
    clearable=False,
    style={"width": "200px", "marginBottom": "20px"}
)

regionPickerWrapper = html.Div(
    regionPicker,
    style={"display": "flex", "justifyContent": "center"}
)


@app.callback(
    Output(visualization, "figure"),
    Input(regionPicker, "value")
)

def update_graph(region):
    # filter the dataset
    if region == "all":
        trimmed_data = data
    else:
        trimmed_data = data[data["region"] == region]

    # generate a new line chart with the filtered data
    figure = chartGeneration(trimmed_data)
    return figure









app.layout = html.Div(
    [
        title,
        regionPickerWrapper,
        visualization
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": COLORS["primary"], 
        "padding": "20px"}
)


if __name__ == '__main__':
    app.run()