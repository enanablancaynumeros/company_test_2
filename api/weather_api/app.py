import os

from flask import Flask, jsonify, redirect
import dash
import dash_core_components as dcc
import dash_html_components as html

from connectors.db_connection import create_db_if_not_exists

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["API_SECRET_KEY"]
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_route = '/plotly_map/'
dash_app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=app,
    url_base_pathname=dash_route
)


@app.route("/_internal_/health")
def flask_api_health():
    return jsonify(msg="ok")


@app.cli.command()
def alembic_autogenerate_revision():
    from alembic_scripts.utils import generate_migration_script

    generate_migration_script()


@app.cli.command()
def create_database_and_upgrade():
    from alembic_scripts.utils import alembic_upgrade_head

    create_db_if_not_exists()
    alembic_upgrade_head()


@app.route('/map/')
def render_dashboard():
    return redirect(dash_route)


def get_data():
    from handlers.db.stations_model import DBStationsHandler
    all_stations = DBStationsHandler.get_all()
    latitudes = [station["latitude"] for station in all_stations]
    longitudes = [station["longitude"] for station in all_stations]
    station_names = [station["station_name"] for station in all_stations]
    return latitudes, longitudes, station_names


def get_figure():
    latitudes, longitudes, station_names = get_data()
    return dict(
        data=[
            dict(
                type="scattergeo",
                lon=longitudes,
                lat=latitudes,
                text=station_names,
                mode="markers",
                marker=dict(
                    size=2,
                    opacity=0.8,
                    reversescale=True,
                    autocolorscale=False,
                    symbol="square",
                    line=dict(width=1, color="rgba(102, 102, 102)"),
                    colorscale=[
                        [0, "rgb(5, 10, 172)"],
                        [0.35, "rgb(40, 60, 190)"],
                        [0.5, "rgb(70, 100, 245)"],
                        [0.6, "rgb(90, 120, 245)"],
                        [0.7, "rgb(106, 137, 247)"],
                        [1, "rgb(220, 220, 220)"],
                    ],
                    cmin=0,
                    colorbar=dict(title="Stations"),
                ),
            )
        ],
        layout=dict(
            title="Weather stations in Germany",
            colorbar=True,
            geo=dict(
                scope="europe",
                showland=True,
                showlegend=False,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=1.0,
                subunitwidth=1.0,
            ),
        ),
    )


def build_layout():
    return html.Div(
        [
            html.H1(children="Weather stations in Germany"),
            html.Div(
                [
                    dcc.Graph(
                        id="map-graph", figure=get_figure(), style={"height": "1000px"}
                    )
                ]
            ),
        ]
    )


dash_app.layout = build_layout
