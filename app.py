import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for home page...")
    return (
        f"Hawaiian Weather API <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     session = Session(engine)
#     prcp_12 = session.query(Measurement.prcp, Measurement.date)
#     return jsonify

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()

    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Find date 12 months back
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]

    year = int(last_date[:4])
    month = int(last_date[5:7])
    day = int(last_date[8:])
    start_date = dt.date(year, month, day) - dt.timedelta(days=365)

    # Find most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    first_station = station_activity[0][0]

    # Retrieve temperatures for this station for the last year of data
    tobs_station_12 = session.query(Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == first_station).\
        order_by(Measurement.date).all()

    session.close()

    station_data_12 = list(np.ravel(tobs_station_12))
    return jsonify(station_data_12)

if __name__ == "__main__":
    app.run(debug=True)