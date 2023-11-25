# https://ikus.pesc.ru/
# -*- coding: utf-8 -*-
import requests
import sys
import json

class IKUS_API:

    def __init__(self, timeout=15.0):
        """
        """
        self.timeout = timeout
        self.account_page = ''
        self.cookie = ''
        self.access = ''
        self.auth = ''
        self.sess = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Captcha': 'none',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
            'customer': 'ikus-spb',
            'Origin': 'https://ikus.pesc.ru',
            'Referer': 'https://ikus.pesc.ru/indications/individual/accounts?id=2434337',
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
        cookies=r.headers['Set-Cookie'].split(';')[0]
        self.headers['Cookie']=cookies

        formdata = {
            "type": "PHONE",
            "login": kwargs.get('username'),
            "password": kwargs.get('password')
        }

        json_data = json.dumps(formdata)
        r = self.sess.post(f"{data['domain']}/api/v7/users/auth",
                           allow_redirects=False,
                           data=json_data,
                           headers=self.headers,
                           timeout=self.timeout)
        response_json = json.loads(r.content)
        auth_token = response_json.get('auth')
        self.access = response_json.get('access')
        self.auth = auth_token

        self.headers['Authorization']='Bearer ' +auth_token
        assert r.ok, 'Ошибка авторизации'
  
        r = self.sess.get(f"{data['domain']}/api/v6/accounts/2434337/meters/info",
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def send_values(self,**kwargs):
        body = [
            {
                "scaleId": 1,
                "value": int(kwargs.get('energo_counter_value'))
            }
        ]

        #отправляем показания
        r = self.sess.post(f"{data['domain']}/api/v6/accounts/2434337/meters/26833261/reading",
                           data=json.dumps(body),
                           headers=self.headers,
                           timeout=self.timeout)
        
        if r.status_code == 200:
            print('Показания успешно переданы')
        else:
            print(r.content)
            print(r.status_code)

    def logout(self):
        body = {
            "access": self.access,
            "auth": self.auth,
        }
        r = self.sess.delete(f"{data['domain']}/api/v6/users/auth",
                          headers=self.headers,
                          data=json.dumps(body),
                          timeout=self.timeout)
        assert r.ok
        if r.status_code == 200:
            print('Выход выполнен')
if __name__ == '__main__':
    data = {
        'username': '',
        'password': '',
        'energo_counter_value':'',
    }

    api = IKUS_API()
    try:
        data['domain'] = 'https://ikus.pesc.ru'
        data['username']=str(sys.argv[1])
        data['password']=str(sys.argv[2])
        data['energo_counter_value']=str(sys.argv[3])             
        #call function
        api.login(**data)
        api.send_values(**data)

    finally:
        api.logout()
        print('close connection')