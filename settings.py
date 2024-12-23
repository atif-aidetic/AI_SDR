from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass
class ENV:
    def __init__(self):
        self.APOLLO_AUTH_KEY = os.getenv("APOLLO_AUTH_KEY")
        self.apollo_company_search = os.getenv("apollo_company_search")
        self.apollo_people_search = os.getenv("apollo_people_search")
        self.linkedin_proxy_curl_api_key = os.getenv("linkedin_proxy_curl_api_key")
        self.linkedin_api_endpoint = os.getenv("linkedin_api_endpoint")
        self.news_api = os.getenv("news_api")
        self.openai_api_key = os.getenv("openai_api_key")
        self.google_api_key = os.getenv("google_api_key")
        self.google_cse_id = os.getenv("google_cse_id")
        self.insight_data_api = os.getenv("insight_data_api")
        self.cold_data_api = os.getenv("cold_data_api")
        
    def print_all(self):
        for key, value in self.__dict__.items():
            print(f'{key}: {value}')

env = ENV()