import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
import database

def preprocess():
    url= "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
    querystring = {"Scheme_Type":"Open"}

    headers = {
	    "x-rapidapi-key": "b4e8a7b16cmsheeec900dd03cf70p1f3a47jsn029b022b43a4",
	    "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    response=response.json()
    for scheme in response:
        database.insert_fund_family_details(str(scheme['Scheme_Code']),scheme['Scheme_Name'],
                                            scheme['Net_Asset_Value'],scheme['Scheme_Type'],
                                            scheme['Mutual_Fund_Family'])
        
    
preprocess()
scheduler=BackgroundScheduler()
scheduler.add_job(preprocess,'cron',minute='*/59')