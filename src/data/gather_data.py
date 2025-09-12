import requests
import sqlalchemy
import sys
import os
# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src')) # this makes it so i can do imports correctly, cannot figure out why it isnt working otherwise.

from src.api.config import settings


scheduleURL = f"https://baker-api.sportsdata.io/baker/v2/nfl/projections/players/full-season/2025REG/avg?key={settings.API_KEY}"

schedule_response = requests.get(scheduleURL)

print(schedule_response.content) # This correctly extracts all of the data.

