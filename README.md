fogbugz
=======

Query fogbugz to get bug summaries


Requirements:
_____________

Python 3
Python Packages: requests, beautifulsoup4, datetime, lxml


Usage:
______
Edit the token_string variable to specify your Fogbugz token

The script writes output to csv files in app/static/data Adjust path if needed

Currently the script summarizes for current, last 1 week, last 1 month, YTD and last 1 year time frames. 
