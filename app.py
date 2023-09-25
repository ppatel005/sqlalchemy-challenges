# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, text, and_
from datetime import datetime, timedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
database = automap_base()

# reflect the tables
database.prepare(autoload_with=engine)

# Save references to each table
Measurement = database.classes.measurement
Station = database.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation") 
def precipitation():
        most_recent = session.query(func.max(Measurement.date))[0]
        most_recent = datetime.strptime(most_recent, '%Y-%m-%d')
        one_year = most_recent - timedelta(days=365)
        query_result = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_result, Measurement.prcp).all()
        prcp_dict = dict()
        for row in query_result:
            prcp_dict[row[0]] = row[1]
        return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station_list():
    station_query = session.query(Station.station)
    station_list = list()
    for row in station_query:
        station_list.append(row[0])
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def station_temp_data():
    most_active_station = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()[0]
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station) 

    temp_list = list()
    for row in temperature_data:
        temp_list.append(row[0])
    return jsonify(temp_list)

@app.route("/api/v1.0/start_date")
def start_stats():
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter
    (Measurement.date >= start_date)

    temp_data = list()
    for row in temp_data:
        for elem in row:
            temp_data.append(elem)
    return jsonify(list(temp_data)) 

@app.route("/api/v1.0/start_date/end_date")
def start_end_stats():
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter
    (Measurement.date >= start_date).filter(Measurement.date<= end_date)

    temp_data = list()
    for row in temp_data:
        for elem in row:
            temp_data.append(elem)
    return jsonify(list(temp_data))

if __name__ == "__main__":
    app.run(debug=True)

