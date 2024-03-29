FROM python:3.7.3

RUN apt-get update
RUN pip install uvloop

ADD . /var/www/hw1

WORKDIR /var/www/hw1

EXPOSE 80

VOLUME  ["/etc/httpd.conf"]

CMD python3 main.py --config-file /etc/httpd.conf