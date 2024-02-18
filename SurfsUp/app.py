# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement =  Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end<br/>"
    )



#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    results=session.query(Measurement.date,Measurement.prcp).all()
    date_prec = []
    for date,prec in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["precipitation"] = prec
        date_prec.append(prec_dict)
    return jsonify(date_prec)  
@app.route("/api/v1.0/stations")
def stations():
    station_names=session.query(Station.name).all()
    names = list(np.ravel(station_names))
    return jsonify(names)
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=366)
    date_tobs = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > year_ago).filter(Measurement.station=='USC00519281').all()
    tob_list=[]
    for date,tob in date_tobs:
        tob_list.append(tob)
    return jsonify(tob_list)
session.close()
if __name__ == '__main__':
    app.run(debug=True)
