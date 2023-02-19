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
        :param login:
        :param password:
        :return:
        """
        r = self.sess.get('https://lk.itpc.ru/',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok

        body=f"login={kwargs.get('username')}&password={kwargs.get('password')}"

        r = self.sess.post('https://lk.itpc.ru/',
                           allow_redirects=False,
                           data=body,
                           headers=self.headers,
                           timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'
        
        r = self.sess.get('https://lk.itpc.ru/#counters',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def send_values(self,**kwargs):
        body =dict()
        body = {
                str(kwargs.get('cold_counter_id')): f"{int(kwargs.get('cold_water_value'))}",
                str(kwargs.get('hot_counter_id')): str(kwargs.get('hot_water_value')),
                str(kwargs.get('electro_counter_day_id')): str(kwargs.get('electro_counter_day_value')),
                str(kwargs.get('electro_counter_night_id')): str(kwargs.get('electro_counter_night_value'))
            }
        self.sendformdata=json.dumps(body)
        r = self.sess.put(kwargs.get('ipulink'),
                           data=self.sendformdata,
                           headers=self.headers,
                           timeout=self.timeout)
        # print(r.content)
        # print(r.status_code)
        assert r.ok, 'Ошибка авторизации'
        if r.status_code == 200:
            print('Показания успешно переданы')
        else:
            print(r)
            print(r.status_code)


    def logout(self):
        r = self.sess.get('https://lk.itpc.ru/logout/',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok
if __name__ == '__main__':
    data = {
        'cold_counter_id': '',
        'hot_counter_id':'',
        'electro_counter_day_id': '',
        'electro_counter_night_id': '',
    }

    api = Voda_API()
    try:
        data['username']=str(sys.argv[1])
        data['password']=str(sys.argv[2])
        data['cold_counter_id']=str(sys.argv[3])
        data['hot_counter_id']=str(sys.argv[4])
        data['cold_water_value']=str(sys.argv[5])
        data['hot_water_value']=str(sys.argv[6])
        data['electro_counter_day_id']=str(sys.argv[7])
        data['electro_counter_night_id']=str(sys.argv[8])
        data['electro_counter_day_value']=str(sys.argv[9])
        data['electro_counter_night_value']=str(sys.argv[10])
        #link send counter values
        data['ipulink']=f"https://lk.itpc.ru/v2/account/{data['username']}/counters/"
        api.login(**data)
        api.send_values(**data)

    finally:
        api.logout()
        print('close connection')