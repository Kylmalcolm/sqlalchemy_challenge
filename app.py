import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime

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

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp)
    session.close()

    prcp_list = []

    for row in prcp_data:
        prcp_dict = {}
        prcp_dict[row[0]] = row[1]
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

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

@app.route("/api/v1.0/<date>")
def stats_temps(date):

    date = datetime.strptime(date, "%Y-%m-%d").date()

    session = Session(engine)

    start_min_avg_max = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs),2), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    session.close()

    return jsonify(start_min_avg_max)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    session = Session(engine)

    min_avg_max = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    if search_term == canonicalized:
        return jsonify(min_avg_max)

    return jsonify({"error": "Date not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)