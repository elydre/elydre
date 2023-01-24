import requests

class Status:
    def __init__(self, url):
        self.url = url
        self.brut = requests.get(url=url).json()

    def refresh(self):
        self.brut = requests.get(url=self.url).json()
    
    def get_status(self, bot_name):
        try: return [b for b in self.brut if b['name'] == bot_name][0]['status']
        except: return "the bot is not on the API"

    def get_role(self, bot_name):
        try: return [b for b in self.brut if b['name'] == bot_name][0]['role']
        except: return "the bot is not on the API"

    def list_bots(self):
        return [b['name'] for b in self.brut]