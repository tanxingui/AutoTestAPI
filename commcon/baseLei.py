from commcon.baseApi import BaseApi


class Add_b(BaseApi):
    def add_b(self):
        resp = self.request_send(file=False)
        return resp

class Add_c(BaseApi):
    def add_c(self):
        resp = self.request_send(file=False)
        return resp

