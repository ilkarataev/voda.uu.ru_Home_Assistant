# lk.itpc.ru_Home_Assistant

Отправка данные счетчиков из Home Assustant на сатй lk.itpc.ru
У меня есть уже данные в Home Assistant, но давно хотел сделать автоматическую отправку показаний. Актуально для жителей Челябинска и области, возможно еще где-то используется сервис lk.itpc.ru. Первое, что нужно сделать - получить номера ИПУ(Смотреть статью). Возможно, в будущем допишу скрипт и это будет делаться автоматически, но сейчас придется делать вручную.  
### Статья 
https://sprut.ai/client/article/4394


Копируем или вставляем файл в /config/python_scripts/counter_sender.py  

Добавляем в configurations.yaml необходимый вариант

```
Вариант 1   
send_water_conters_values: 'python3 /config/python_scripts/counter_sender.py login passs cold_counter_id hot_counter_id {{ states("sensor.water_control_cold_count") }} {{ states("sensor.water_control_hot_count") }} electro_counter_day_id electro_counter_night_id  {{ states("sensor.electro_counter_day_value") }} {{ states("sensor.electro_counter_night_value") }}'  
```

Автоматизация
```
- alias: "Отправка показаний на lk.itpc.ru"
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
Если вы Воспользовались кодом буду признателен за не большой донат, можно сделать на sprut.ai -> Отблагдорить автора.