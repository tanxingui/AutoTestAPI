import requests
from configs.config import NAME_PWD

class Login:
    @classmethod
    def login(cls, data):
        url = 'http://api.s.youcheyihou.com/testapi/iyourcar_autobuy/backend/login'
        res = requests.post(url=url, data=data)
        sid = res.json()["result"]["sid"]
        # token = res.json()["result"]["token"]
        token = str(sid).split('#')[1]
        return token, sid



if __name__ == '__main__':
    print(Login().login(NAME_PWD))
