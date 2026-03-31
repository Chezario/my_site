from t_tech.invest import Client
import os
from .token import INVEST_TOKEN


class ClientWithToken:
    TOKEN = INVEST_TOKEN  # os.getenv("INVEST_TOKEN")

    def get_client(self):
        client_obj = Client(self.TOKEN)
        return client_obj