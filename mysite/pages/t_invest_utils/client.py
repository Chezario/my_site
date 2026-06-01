from t_tech.invest import Client
from .token import INVEST_TOKEN
from dotenv import load_dotenv
import os


load_dotenv()

class ClientWithToken:
    TOKEN = os.getenv("INVEST_TOKEN")
    # TOKEN = INVEST_TOKEN  # os.getenv("INVEST_TOKEN")

    def get_client(self):
        client_obj = Client(self.TOKEN)
        return client_obj