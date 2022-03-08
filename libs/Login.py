import requests
from utils.decorator import show_time


class Login:
    @show_time  # 接口耗时
    def login(self):
        url = 'http://api.s.youcheyihou.com/testapi/iyourcar_autobuy/backend/login'
        data = {
            "data": '{'
                    '"username":"tanxingui",'
                    '"password":"1",'
                    '"captcha_text":"123456",'
                    '"captcha_key":"5a3c82b303c5446a9295eddb134851db"'
                    '}'}
        res = requests.post(url=url, data=data)
        sid = res.json()["result"]["sid"]
        # token = res.json()["result"]["token"]
        token = str(sid).split('#')[1]
        return token, sid

if __name__ == '__main__':
    print(Login().login())
