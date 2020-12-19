
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector


# Multi-dropdown options
from GOP.dashboard.controls import operations


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

#DATABASE
cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                              host='89.252.185.4',
                              database='bytechde_airport_comp491')
cursor = cnx.cursor()



# Create controls
ops = [
    {"label": str(o), "value": str(operations[o])} for o in operations
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
                        html.Div(
                            [
                                html.H3(
                                    "Ground Operations Data",
                                    style={"margin-bottom": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by operation (or select range in histogram):",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="day_slider",
                            min=1,
                            max=30,
                            value=[1, 4],
                            className="dcc_control",
                        ),
                        html.P("Filter by operation:", className="control_label"),
                        dcc.Dropdown(
                            id="operations",
                            options=ops,
                            multi=False,
                            value=[operations.get(a) for a in operations.keys()],
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
                                    [html.H6(id="planes_text"), html.P("Planes")],
                                    id="planes",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="flight_text"), html.P("Delayed Flights")],
                                    id="flight",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Customer Complaints")],
                                    id="water",
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
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
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
    ],
)
def update_total_text(day_slider):

    query= """SELECT * FROM ground_operation WHERE plane_parked <= """+""""2020-12-"""+str(day_slider[-1])+"""" AND plane_parked >= """+""""2020-12-"""+str(day_slider[0])+"""" """
    print(query)
    cursor.execute(query)
    selectedOps=cursor.fetchall()
    return selectedOps.__len__()


@app.callback(
    Output("waterText", "children"),
    [
        Input("operations", "value"),
        Input("day_slider", "value"),
    ],
)
def update_customer_text(operations,day_slider):
    print(operations)
    print(day_slider)
    return human_format(day_slider[-1])

@app.callback(
    Output("flight_text", "children"),
    [
        Input("day_slider", "value"),
    ],
)
def update_flight_text(day_slider):
    query = """SELECT * FROM flight WHERE planned_departure_time <= """ + """"2020-12-""" + str(
        day_slider[-1]) + """" AND planned_departure_time >= """ + """"2020-12-""" + str(day_slider[0]) + """" AND is_delayed = "Y" """
    print(query)
    cursor.execute(query)
    selectedFlights = cursor.fetchall()
    return selectedFlights.__len__()

@app.callback(
    Output("planes_text", "children"),
    [
        Input("day_slider", "value"),
    ],
)
def update_planes_text(day_slider):
    query = """SELECT * FROM flight WHERE planned_departure_time <= """ + """"2020-12-""" + str(
        day_slider[-1]) + """" AND planned_departure_time >= """ + """"2020-12-""" + str(day_slider[0]) + """" """
    print(query)
    #cursor.execute(query)
    #selectedPlanes = cursor.fetchall()
    return "0"#selectedPlanes.__len__()



if __name__ == "__main__":
    app.run_server()
