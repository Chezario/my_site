from t_tech.invest import Client
import os


class ClientWithToken:
    TOKEN = os.getenv("INVEST_TOKEN")

    def get_client(self):
        client_obj = Client(self.TOKEN)
        return client_obj