# Summary #
This project analyzes the climate of Honolulu, Hawaii provided in a SQLite database. The database provides datapoints across 9 stations where precipitation (in inches) and temperatures (in farenehit) are observed over 17 years (2010-2017) in Honolulu.  SQLAlchemy was used to translate python querying to the SQLite database. The resulting precipitation and temperatures of the last year were plotted using Matplotlib. 

The results queries were then translated into a Flask app to create endpoints that other users can use to view the data for precipitation, temperature observations, and stations for the last year of data. Additionally, two endpoints allow users to dynamically enter a given start date or a date range to query min, max, and average temperatures for those dates. 

See included Jupyter notebook and app.py file for details and conclusions.

# Note on using endpoints #
## Precipitation, temperature observations, and stations endpoints ##
Links are provided on the home page for precipitation, temperature observations, and stations or the listed texts can be copied and pasted after the home url in the browser to reach the same destination. These endpoints will return datapoints for the last year in the dataset. 

## Endpoints using start date or date rante (i.e., start and end date) ##
### Start date ###
Providing a start date will return min, max, and average temperatures for all dates after and including the given start date. To use this endpoint, please paste in the date in YYY-MM-DD format at the end of the start date endpoint. For example: /api/v1.0/start/2016-08-23.

### Date range (i.e., start and end date) ###
Providing a date range will return min, max, and average temperatures for all dates within the range, including the given start and end dates. To use this endpoint, please paste in the date in YYY-MM-DD format, with the start of the date range after 'start and end of the date range after 'end'. For example: /api/v1.0/start/2016-08-23/end/2017-08-23.

# Tools Used #
Python, Pandas, SQLAlchemy, Matplotlib, Numpy, Flask

# Acknowledgments #
I used online resources (Stack Overflow, etc.) and chatted with colleagues for debugging of similar issues.