import os
import logging
import json
import requests

api_key = os.getenv("OPENAI_API_KEY")

class TravelPlannerAgent:
    def __init__(self, model, api_key) -> None:
        self.model = model
        self.api_key = api_key

    def load_schema(self):
        with open('schema.json', 'r') as schema_file:
            return json.load(schema_file)

    def get_prompt(self, travel_dest, duration) -> str:
        schema = self.load_schema()
        return f"""You are a travel itinerary planner. Given the parameters TRAVEL_DEST={travel_dest} and DURATION={duration}, provide a travel itinerary. Include top attractions, experiences, and activities with coordinates and broken out by time of day. Provide output in valid JSON in the form of the following schema {json.dumps(schema)}"""

    def get_recommendations(self, days, location_str) -> str:
        prompt = self.get_prompt(location_str, days)
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': self.model,
            'messages': [{"role": "user", "content": prompt}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        try:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"API Call Failed: {e}, Response Status: {response.status_code}, Response Text: {response.text}")
            return None


