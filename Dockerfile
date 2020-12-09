FROM python

WORKDIR /monitor

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD src .

VOLUME [ "/monitor/config" ]
