### Проект "Event planning"

Тестовый проект на Django для ознакомления с возможностями фреймворка. 
Концепция: 
Организаторы могут создавать различные мероприятия в залах или комнатах. На эти мероприятия могут записываться посетители. За какой-то период до мероприятия происходит рассылка уведомлений на e-mail посетителей. По окончанию мероприятия, оно становится неактивным, а место в комнате освобождается.

Приложение на Django запускается под виртуальной оболочной проекта из главной директорией проекта следующей командой:
```bash
python manage.py runserver
```
Рассылка уведомлений основана на Celery. Бэком для него выступает Redis.
Эта задача запускается при старте Celery и работает до остановки Celery. Раз в какое-то время (***SECONDS_FOR_WAIT***) задача запускается и получает мероприятия в промежутке от времени пробуждения до заданного времени до мероприятия (***PRE_EVENT_TIME_SECONDS***). Для всех полученных мероприятий происходит рассылка посетителям и ставится статус произошедшей рассылки, для избежания повторной рассылке по мероприятию.
Celery запускается под виртуальной оболочной проекта из главной директорией проекта следующей командой:
```bash
celery -A event_planning worker -E -l info
```
Константы ***SECONDS_FOR_WAIT*** и ***PRE_EVENT_TIME_SECONDS*** задаются в файле "***planning/tasks.py***" в виде секунд