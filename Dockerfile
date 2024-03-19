FROM python
WORKDIR Users/user/PycharmProjects/event_planning
COPY requirements.txt ./
RUN pip install -r requirements.txt
