# -*- coding: utf-8 -*-
import requests
from datetime import datetime, date, time
import sys
import re

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
        r = self.sess.get('https://lk.voda.uu.ru/login',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok

        formdata = dict()
        formdata['j_username'] = kwargs.get('username')
        formdata['j_password'] = kwargs.get('password')
        r = self.sess.post('https://lk.voda.uu.ru/j_spring_security_check',
                           allow_redirects=False,
                           data=formdata,
                           headers=self.headers,
                           timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def no_login(self, **kwargs):
        """
        :param account:
        :param numer of building:
        :param apartment:
        :return:
        """
        r = self.sess.get('https://lk.voda.uu.ru/login',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok

        formdata = dict()
        formdata['j_account'] = kwargs.get('account')
        formdata['j_building'] = kwargs.get('building')
        formdata['j_apartment'] = kwargs.get('apartment')
        formdata['j_login_ipu'] = '1'
        formdata['submit'] = ''
        r = self.sess.post('https://lk.voda.uu.ru/protected_ipu/logon',
                           allow_redirects=False,
                           data=formdata,
                           headers=self.headers,
                           timeout=self.timeout)
        assert r.ok, 'Ошибка авторизации'

    def send_values(self,login_mode,**kwargs):
        body_cold = dict()        
        body_hot = dict()        
        body_cold['input_date'] = str(date.today().strftime("%d.%m.%Y"))
        body_hot['input_date'] = str(date.today().strftime("%d.%m.%Y"))
        if login_mode == 'login':
            body_cold['counters_list[]'] = str(kwargs.get('cold_counter_id'))
            body_cold['readings_list[]'] = str(kwargs.get('cold_water_value'))
            body_hot['counters_list[]'] = str(kwargs.get('hot_counter_id'))
            body_hot['readings_list[]'] = str(kwargs.get('hot_water_value'))
        else:
            body_cold['counters_list'] = str(kwargs.get('cold_counter_id'))
            body_cold['readings_list'] = str(kwargs.get('cold_water_value'))
            body_hot['counters_list'] = str(kwargs.get('hot_counter_id'))
            body_hot['readings_list'] = str(kwargs.get('hot_water_value'))
        self.sendformdata=body_cold
        r_cold = self.sess.post(kwargs.get('ipulink'),
                           data=self.sendformdata,
                           headers=self.headers,
                           timeout=self.timeout)
        assert r_cold.ok, 'Ошибка авторизации'
        if r_cold.status_code == 200:
            print('Показания счетчика холодной воды успешно переданы')
        self.sendformdata=body_hot
        r_hot = self.sess.post(kwargs.get('ipulink'),
                           data=self.sendformdata,
                           headers=self.headers,
                           timeout=self.timeout)
        if r_hot.status_code == 200:
            print('Показания счетчика горячей воды успешно переданы')
        assert r_hot.ok, 'Ошибка авторизации'

    def logout(self, **kwargs):
        r = self.sess.get('https://lk.voda.uu.ru/logoff',
                          headers=self.headers,
                          timeout=self.timeout)
        assert r.ok
if __name__ == '__main__':
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    data = {
        'cold_counter_id': '',
        'hot_counter_id':'',
    }

    api = Voda_API()
    try:
        if(re.fullmatch(email_regex, sys.argv[1])):
            data['username']=str(sys.argv[1])
            data['password']=str(sys.argv[2])
            data['cold_counter_id']=str(sys.argv[3])
            data['hot_counter_id']=str(sys.argv[4])
            data['cold_water_value']=str(sys.argv[5])
            data['hot_water_value']=str(sys.argv[6])
            data['ipulink']='https://lk.voda.uu.ru/protected/input'
            print("login_mode")
            api.login(**data)       
            api.send_values('login',**data)
        else:
            data['account']=str(sys.argv[1])
            data['building']=sys.argv[2]
            data['apartment']=str(sys.argv[3])
            data['cold_counter_id']=str(sys.argv[4])
            data['hot_counter_id']=str(sys.argv[5])
            data['cold_water_value']=str(sys.argv[6])
            data['hot_water_value']=str(sys.argv[7])
            data['ipulink']='https://lk.voda.uu.ru/protected_ipu/input'            
            print("no_login_mode")
            api.no_login(**data)       
            api.send_values('no_login',**data)
    
    finally:
        api.logout()
        print('close')