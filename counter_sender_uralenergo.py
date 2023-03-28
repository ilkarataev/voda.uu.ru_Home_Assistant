# -*- coding: utf-8 -*-
import json
import requests
import sys

# -------------- Voda_API ----------------------
class Voda_API:

    def __init__(self, timeout=15.0):
        """
        """
        self.timeout = timeout
        self.account_page = ''
        self.cookie = ''
        self.sess = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.sendformdata = {}

    def login(self, **kwargs):
        """
        :param userid:
        :return:
        """
    
        r = self.sess.get('https://eirc.uralsbyt.ru/?wg=02',
                          headers=self.headers,
                          timeout=self.timeout)
        
        cookies=r.headers['Set-Cookie'].split(';')[0]
        self.headers['Cookie']=cookies
        assert r.ok

        body=f"wg=02&login={kwargs.get('username')}&password={kwargs.get('password')}"

        r = self.sess.post('https://eirc.uralsbyt.ru/login',
                           allow_redirects=False,
                           data=body,
                           headers=self.headers,
                           timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'
        
        r = self.sess.get('https://eirc.uralsbyt.ru/account',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def send_values(self,**kwargs):
        body = f"de[]={kwargs.get('hot_water_counter_id')}&val[]={kwargs.get('hot_water_value')}"
        self.sendformdata=body

        #отправляем показания
        r = self.sess.post(kwargs.get('ipulink'),
                           data=self.sendformdata,
                           headers=self.headers,
                           timeout=self.timeout)
        # print(r.content)
        assert r.ok, 'Ошибка авторизации'
        if r.status_code == 200:
            print('Показания успешно переданы')
        else:
            print(r)
            print(r.status_code)

    def logout(self):
        r = self.sess.get('https://eirc.uralsbyt.ru/logout',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok
if __name__ == '__main__':
    data = {
        'username': '',
        'password': '',
        'hot_water_counter_id':'',
        'hot_water_value': '',
        'energo_counter_value':'',
    }

    api = Voda_API()
    try:
        data['username']=str(sys.argv[1])
        data['password']=str(sys.argv[2])
        data['hot_water_counter_id']=str(sys.argv[3])
        data['hot_water_value']=str(sys.argv[4])
        # data['energo_counter_value']=str(sys.argv[5])
        # data['energo_counter_value']=str(sys.argv[6])
        #link send counter values
        data['ipulink']="https://eirc.uralsbyt.ru/deviceaction"
        api.login(**data)
        api.send_values(**data)

    finally:
        api.logout()
        print('close connection')