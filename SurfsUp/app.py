# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():

    """List all available api routes"""
    return(

        f'Here are all the available API routes:<br/>'
        f'<br/>'
        f'<p><span style = "color: blue;">/api/v1.0/precipitation</span></p>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/precipitation">Click here for precipitation API</a>'
      
        f'<p><span style = "color: blue;">/api/v1.0/stations</span></p>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/stations">Click here for stations API</a>'

        f'<p><span style = "color: blue;">/api/v1.0/tobs</span></p>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/tobs">Click here for temperature observations (tobs) API</a>'
        f'<br/>'
        f'<br/>For below dates, please use date format YYYY-MM-DD when providing a start date or between start and end dates at the end of the url like so:<br/>'
        f'<br/>"/api/v1.0/start/YYYY-MM-DD". This will return min, max, avg. temperature observations for all dates after and including the given start date.<br/>'
        f'<p><span style = "color: blue;">/api/v1.0/start/<start></span></p><br/>'
        f'"/api/v1.0/start/YYYY-MM-DD/end/YYYY-MM-DD". This will return min, max, avg. temperature observations for the given date range.<br/>'
        f'<p><span style = "color: blue;">/api/v1.0/start/<start>/end/<end></span></p><br/>'
    )

@app.route('/api/v1.0/precipitation')
def precip():
    #determine most recent date in the data set
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    #query to retrieve the data and precipitation scores
    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= recent_date[0]).\
                filter(Measurement.date >= year_ago).all()
    
     #create dictionary to jsonify
    precip_dict = [{'date': date, 'prcp':precip} for date, precip in precip_results]
    return jsonify(precip_dict)
    


@app.route('/api/v1.0/stations')
def stations():
    #query for list of stations
    stations = session.query(Station.station).all()

    stations_list = [station[0] for station in stations]
    return jsonify(stations_list)

    #for station in stations:

@app.route('/api/v1.0/tobs')
def tobs():
    #most active stations query
    most_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    #most recent date and year-ago date
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    #query for dates and temp observations of most-active station for the previous year of data
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #get most active station
    most_active_id = most_active[0][0]
    #function for min, max, avg temps
    sel = [Measurement.station, 
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    #query last 12 months of tob for most active station
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= recent_date[0]).filter(Measurement.date >= year_ago).\
                filter(Measurement.station == most_active[0][0]).all()
    
    #create dictionary to jsonify
    temp_dict = [{'date': date, 'temp':temp} for date, temp in temp_results]
    return jsonify(temp_dict)

@app.route('/api/v1.0/start/<start>')
def start_date(start):
     #function for min, max, avg temps
    sel_1 = [Measurement.date, 
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    #filter temp for all dates including and after given start date
    start_temps = session.query(*sel_1).filter(Measurement.date >= start).group_by(Measurement.date).all()

     #create dictionary to jsonify
    start_temp_dict = [{'date':date, 'min. temp.':min, 'max. temp.':max, 'avg. temp.':avg} for date, min, max, avg in start_temps]
    return jsonify(start_temp_dict)

@app.route('/api/v1.0/start/<start>/end/<end>')
def start_end(start, end):
    #function for min, max, avg temps
    sel_2 = [Measurement.date, 
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    #filter temp for all dates in given date rate, inclusive
    start_end_temps = session.query(*sel_2).filter(Measurement.date >= start).filter(Measurement.date <= end).\
                    group_by(Measurement.date).all()
    
     #create dictionary to jsonify
    start_end_dict = [{'date':date, 'min. temp.':min, 'max. temp.':max, 'avg. temp.':avg} for date, min, max, avg in start_end_temps]
    return jsonify(start_end_dict)



if __name__ == '__main__':
    app.run(port = 5000, debug = True)

session.remove()

