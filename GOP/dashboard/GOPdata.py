
import copy
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector

operations={
    "Boarding":1,
    "Baggage":2,
    "Catering":3,
    "Parking":4
}

months={
    1:"January",
    2:"Febuary",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December"
}

years={
    2020:"2020",
    2019:"2019",
    2018:"2018",
    2017:"2017",
    2016:"2016",
}

standardTimes={
    60:"60",
    65:"65",
    70:"70",
    75:"75",
    80:"80",
    85:"85",
    90:"90",
    95:"95",
    100:"100",
    105:"105",
    110: "110",
    115: "115",
    120: "120",
    125: "125",
    130: "130",
    135: "135",
    140: "140",
    145: "145",
    150: "150",
    155: "155",
    160: "160",
    165: "165",
    170: "170",
    175: "175",
}


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

#DATABASE
cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                              host='89.252.185.4',
                              database='bytechde_airport_comp491')


df_flight = pd.read_sql_query("""SELECT * FROM flight""", cnx)
df_airports=pd.read_sql_query("""SELECT * FROM aiport""", cnx)
df_planes=pd.read_sql_query("""SELECT * FROM plane""", cnx)
df_operations=pd.read_sql_query("""SELECT * FROM ground_operation""", cnx)

op_table_names=[["boarding_started","boarding_ended"],["baggage_started","baggage_ended"],["catering_service_started","catering_service_ended"],["plane_parked","plane_pushback"]]


# Create controls
ops = [
    {"label": str(o), "value": operations[o]} for o in operations
]
month_ops = [
    {"label": str(months[m]), "value": m}
    for m in months
]
year_ops = [
    {"label": str(years[y]), "value": y}
    for y in years
]
standard_ops = [
    {"label": str(standardTimes[y]), "value": y}
    for y in standardTimes
]

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h")
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by day (1-31):",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="day_slider",
                            min=1,
                            max=31,
                            value=[1, 4],
                            className="dcc_control",
                        ),
                        html.P("Filter by Month", className="month_label"),
                        dcc.Dropdown(
                            id="month",
                            options=month_ops,
                            multi=False,
                            value=12,
                            className="dcc_control",
                        ),
                        html.P("Filter by Year", className="year_label"),
                        dcc.Dropdown(
                            id="year",
                            options=year_ops,
                            multi=False,
                            value=2020,
                            className="dcc_control",
                        ),
                        html.P("Filter by operation:", className="control_label"),
                        dcc.Dropdown(
                            id="operations",
                            options=ops,
                            multi=False,
                            value=4,
                            className="dcc_control",
                        ),
                        html.P("Standard apron time for operations", className="standard_label"),
                        dcc.Dropdown(
                            id="standard",
                            options=standard_ops,
                            multi=False,
                            value=100,
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="total_text"), html.P("Total Operations")],
                                    id="totalOps",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="planes_text"), html.P("Total Flights")],
                                    id="planes",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="flight_text"), html.P("Delayed Flights")],
                                    id="flight",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="percent_text"), html.P("Total Delay Time (minutes)")],
                                    id="hour",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [dcc.Graph(id="pie_graph")],
        #             className="pretty_container seven columns",
        #         ),
        #         html.Div(
        #             [dcc.Graph(id="aggregate_graph")],
        #             className="pretty_container five columns",
        #         ),
        #     ],
        #     className="row flex-display",
        # ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# Helper functions
def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]


def filter_operations(df, day_slider,month,year):
    dff = df[
        (df["plane_parked"] >= dt.datetime(year,month,day_slider[0]))
        & (df["plane_parked"] <= dt.datetime(year,month,day_slider[1], 23,59,59))
    ]
    return dff

def filter_flight(df, day_slider,month,year):
    dff = df[
        (df["planned_departure_time"] >= dt.datetime(year,month,day_slider[0]))
        & (df["planned_departure_time"] <= dt.datetime(year,month,day_slider[1], 23,59,59))
    ]
    return dff


# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)


# Selectors -> well text
@app.callback(
    Output("total_text", "children"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
    ],
)
def update_total_text(day_slider,month,year):

    selectedOps=filter_operations(df_operations,day_slider,month,year)
    return len(selectedOps.index)


@app.callback(
    Output("percent_text", "children"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
    ],
)
def update_customer_text(day_slider,month,year):
    selectedFlights = filter_flight(df_flight, day_slider, month, year)
    delays=selectedFlights[selectedFlights["is_delayed"] == "Y"]
    totalDelay=0
    for (column,data) in delays.iteritems():
        if column=="delay_time":
            for d in data.values:
                totalDelay+=d
    return totalDelay

@app.callback(
    Output("flight_text", "children"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
    ],
)
def update_flight_text(day_slider,month,year):
    selectedFlights = filter_flight(df_flight,day_slider,month,year)
    return len(selectedFlights[selectedFlights["is_delayed"]=="Y"].index)

@app.callback(
    Output("planes_text", "children"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
    ],
)
def update_planes_text(day_slider,month,year):
    selectedPlanes = filter_flight(df_flight,day_slider,month,year)
    return len(selectedPlanes.index)


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
        Input("operations","value")
    ],
)
def make_count_figure(day_slider, month, year,operations):

    layout_count = copy.deepcopy(layout)

    dff = filter_operations(df_operations, day_slider, month, year)
    x = [dt.datetime(year,month,day) for day in range(day_slider[0],day_slider[1]+1)]
    y = [0 for _ in range(day_slider[0],day_slider[1]+1)]
    y_i = 0
    ind=0
    for day in range(day_slider[0],day_slider[1]+1):
        nextDay=dt.datetime(year,month,day)+dt.timedelta(days=1)
        g=dff[
          (dff[op_table_names[operations-1][1]]>=dt.datetime(year,month,day))
           & (dff[op_table_names[operations-1][1]]<nextDay)
           ]
        for (index,row) in g.iterrows():
            y_i+=(row[op_table_names[operations-1][1]]-row[op_table_names[operations-1][0]]).seconds/60

        if len(g.index)==0:
            y[ind]=y_i
        else:
            y[ind] = y_i/len(g.index)
        ind+=1
        y_i=0

    colors = []
    for i in range(1, 30):
        if i >= int(day_slider[0]) and i < int(day_slider[1]):
            colors.append("rgb(123, 199, 255)")
        else:
            colors.append("rgba(123, 199, 255, 0.2)")

    data = [
        dict(
            type="bar",
            x=x,
            y=y,
            name="all flights",
            marker=dict(color=colors),
        ),
    ]

    layout_count["title"] = "Operation Average Time in Minutes/Day"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = False
    layout_count["autosize"] = True

    figure = dict(data=data, layout=layout_count)
    return figure

# Main graph -> individual graph
@app.callback(
    Output("individual_graph", "figure"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
    ],
)
def make_individual_figure(day_slider, month, year):

    layout_individual = copy.deepcopy(layout)

    dff = filter_operations(df_operations, day_slider, month, year)
    x = [dt.datetime(year, month, day) for day in range(day_slider[0], day_slider[1] + 1)]
    y = [0 for _ in range(day_slider[0], day_slider[1] + 1)]
    y_i = 0
    ind = 0
    y_tot={}
    y_tot[op_table_names[0][0]] = [0 for _ in range(day_slider[0], day_slider[1] + 1)]
    y_tot[op_table_names[1][0]] = [0 for _ in range(day_slider[0], day_slider[1] + 1)]
    y_tot[op_table_names[2][0]] = [0 for _ in range(day_slider[0], day_slider[1] + 1)]
    for op in op_table_names:
        if op[0]=="plane_parked":
            continue
        for day in range(day_slider[0], day_slider[1] + 1):
            nextDay = dt.datetime(year, month, day) + dt.timedelta(days=1)
            g = dff[
                (dff[op[1]] >= dt.datetime(year, month, day))
                & (dff[op[1]] < nextDay)
                ]
            for (index, row) in g.iterrows():
                y_i += (row[op[0]]-row[op_table_names[3][0]]).seconds / 60

            if len(g.index) == 0:
                y_tot[op[0]][ind] = y_i
            else:
                y_tot[op[0]][ind] = y_i / len(g.index)
                print(g.index)
            ind += 1
            y_i = 0

        ind=0

    data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Boarding",
                x=x,
                y=y_tot[op_table_names[0][0]],
                line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Baggage",
                x=x,
                y=y_tot[op_table_names[1][0]],
                line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Catering",
                x=x,
                y=y_tot[op_table_names[2][0]],
                line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
                marker=dict(symbol="diamond-open"),
            ),
        ]
    layout_individual["title"] = "Average Time between parking and operations"

    figure = dict(data=data, layout=layout_individual)
    return figure

@app.callback(
    Output("main_graph", "figure"),
    [
        Input("day_slider", "value"),
        Input("month", "value"),
        Input("year", "value"),
        Input("standard", "value"),
    ],
)
def make_main_figure(day_slider, month, year,standard):
    layout_main = copy.deepcopy(layout)

    dff = filter_operations(df_operations, day_slider, month, year)
    x = []
    y = []
    x_above=[]
    y_above=[]


    for (index, row) in dff.iterrows():
        time=(row[op_table_names[3][1]] - row[op_table_names[3][0]]).seconds / 60
        if standard<time:
            y_above.append(time)
            x_above.append(row["operation_id"] - 100000)
        else:
            y.append(time)
            x.append(row["operation_id"]-100000)

    data = [
        dict(
            type="scatter",
            mode="markers",
            x=x,
            y=y,
            name="ops below standard",
            marker=dict(
            color='rgba(0, 152, 0, .8)',
            size=10,
            line=dict(
                color='DarkSlateGrey',
                width=2
            )
            ),
        ),
        dict(
            type="scatter",
            mode="markers",
            x=x_above,
            y=y_above,
            name="ops above standard",
            marker=dict(
                color='rgba(152, 0, 0, .8)',
                size=10,
                line=dict(
                    color='DarkSlateGrey',
                    width=2
                )
            ),
        ),
    ]


    layout_main["title"] = "Operation Time in Minutes"
    layout_main["showlegend"] = True

    figure = dict(data=data, layout=layout_main)
    return figure





if __name__ == "__main__":
    app.run_server()
