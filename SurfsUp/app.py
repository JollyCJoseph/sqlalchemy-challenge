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
        f"Welcome<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br> "
        f"Manually enter the start and end date(yyyy-mm-dd) choose from 2016-08-23 to 2017-08-23"
    )



#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    date_prec = []
    for date,prec in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["precipitation"] = prec
        date_prec.append(prec_dict)
    return jsonify(date_prec)
  
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel=[Station.name,Station.latitude,Measurement.date,Measurement.tobs]
    station_data=session.query(*sel).filter(Station.station==Measurement.station).all()
    session.close()
    data = list(np.ravel(station_data))
    return jsonify(data)
session.close()
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=366)
    date_tobs = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > year_ago).filter(Measurement.station=='USC00519281').all()
    session.close()
    tob_list=[]
    for date,tob in date_tobs:
        tob_list.append(tob)
    return jsonify(tob_list)
@app.route("/api/v1.0/<start>")
def temp(start):
    session = Session(engine)
    temp_results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).all()
    session.close()
    temparatures = []
    for min, max, avrg in temp_results:
        temp_details = {}
        temp_details["Minimum temparature"] = min
        temp_details["Maximum temparature"] = max
        temp_details["Average temparature"] = avrg
        temparatures.append(temp_details)
   
    return jsonify(temparatures)
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp1(start_date,end_date):
    session = Session(engine)
    temp_results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>start_date) or (Measurement.date<=end_date).all()
    session.close()
    temparatures1 = []
    for min, max, avrg in temp_results:
        temp_details1 = {}
        temp_details1["Minimum temparature"] = min
        temp_details1["Maximum temparature"] = max
        temp_details1["Average temparature"] = avrg
        temparatures1.append(temp_details1) 
    return jsonify(temparatures1)  
if __name__ == '__main__':
    app.run(debug=True)
