# voda.uu.ru_Home_Assistant

Отправка данные счетчиков из Home Assustant на сатй voda.uu.ru
У меня есть уже данные в Home Assistant, но давно хотел сделать автоматическую отправку показаний. Актуально для жителей Челябинска и области, возможно еще где-то используется сервис voda.uu.ru. Первое, что нужно сделать - получить номера ИПУ(Смотреть статью). Возможно, в будущем допишу скрипт и это будет делаться автоматически, но сейчас придется делать вручную.  
### Статья 
https://sprut.ai/client/article/4394


Копируем или вставляем файл в /config/python_scripts/voda_uu_ru.py  

Добавляем в configurations.yaml необходимый вариант

```
Вариант 1   
send_water_conters_values: 'python3 /config/python_scripts/voda_uu_ru.py example@gmail.com email_password 79462304777 79462310777 {{ states("sensor.water_control_cold_count") }} {{ states("sensor.water_control_hot_count") }}'  
Вариант 2
send_water_conters_values: 'python3 /config/python_scripts/voda_uu_ru.py 31406477 77A 137 79462310777 7946230477 {{ states("sensor.water_control_cold_count") }} {{ states("sensor.water_control_hot_count") }}'  
Пример отправки вариант 2
send_water_conters_values: 'python3 /config/python_scripts/voda_uu_ru.py 3140645672 77A 137 79462310777 79462304777 77.247 49.153'
```

Автоматизация
```
- alias: "Отправка показаний на voda.uu.ru"
  trigger:
  - platform: time
    at: '08:00:00'
  condition:
    - condition: template
      # Поменять 20 на необходимую дату 
      value_template: "{{ now().day == 20 }}"
  action:
     - service: shell_command.send_water_conters_values
```

Будет дальнейшая разработка чтобы номер счетчика получать в HA. 
Если вы поспользовались кодом буду признателен за донат, можно сделать на sprut.ai -> Отблагдорить автора.