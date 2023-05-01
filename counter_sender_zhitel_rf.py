#Этот скрипт для сайта #кабинет-жителя.рф
# -*- coding: utf-8 -*-
import requests
import sys
import json
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
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        }
        self.sendformdata = {}

    def login(self, **kwargs):
        """
        :param userid:
        :return:
        """
    
        r = self.sess.get(f"{data['domain']}",
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok
        # body for login
        formdata = dict()
        formdata['username'] = kwargs.get('username')
        formdata['password'] = kwargs.get('password')

        r = self.sess.post(f"{data['domain']}/api/v4/auth/login/",
                           allow_redirects=False,
                           data=formdata,
                           headers=self.headers,
                           timeout=self.timeout)
        cookies=r.headers['Set-Cookie'].split(';')[0]
        self.headers['Cookie']=cookies
        assert r.ok, 'Ошибка авторизации'
        
        r = self.sess.get(f"{data['domain']}/#/meters/list/",
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def send_values(self,**kwargs):
        body=dict()
        body["meters"] = [ \
            {"meter_id": kwargs.get('water_counter_id1'),
            "values": [int(kwargs.get('water_value_id1'))]},
            {"meter_id": kwargs.get('water_counter_id2'),
            "values": [int(kwargs.get('water_value_id2'))]},
            {"meter_id": kwargs.get('water_counter_id3'),
            "values": [int(kwargs.get('water_value_id3'))]},
            {"meter_id": kwargs.get('water_counter_id4'),
            "values": [int(kwargs.get('water_value_id4'))]}]

        self.headers['Content-Type']='application/json;charset=utf-8'

        #отправляем показания
        r = self.sess.post(f"{data['domain']}/api/v4/cabinet/meters/",
                           data=json.dumps(body),
                           headers=self.headers,
                           timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'
        if r.status_code == 200:
            print('Показания успешно переданы')
        else:
            print(r)
            print(r.status_code)

    def logout(self):
        r = self.sess.post(f"{data['domain']}/api/v4/auth/logout/",
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
        # кабинет-жителя.рф
        data['domain'] = 'https://xn----7sbdqbfldlsq5dd8p.xn--p1ai'
        data['username']=str(sys.argv[1])
        data['password']=str(sys.argv[2])
        data['water_counter_id1']=str(sys.argv[3])
        data['water_value_id1']=str(sys.argv[4])
        data['water_counter_id2']=str(sys.argv[5])
        data['water_value_id2']=str(sys.argv[6])
        data['water_counter_id3']=str(sys.argv[7])
        data['water_value_id3']=str(sys.argv[8])
        data['water_counter_id4']=str(sys.argv[9])
        data['water_value_id4']=str(sys.argv[10])                
        #call function
        api.login(**data)
        api.send_values(**data)

    finally:
        api.logout()
        print('close connection')