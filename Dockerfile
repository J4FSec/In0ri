FROM tensorflow/tensorflow

RUN apt update
RUN python3 -m pip install --upgrade pip
RUN apt install -y \
    python-flask \
    python-requests \
    cron \
    chromium-chromedriver \
&& pip install selenium \
&& pip install webdriver-manager \
&& pip install Pillow \
&& pip install python-telegram-bot \
&& pip install flask \  
&& pip install pymongo \
&& pip install python-crontab \
&& pip install pyOpenSSL
COPY . /opt/In0ri
ADD start.sh /start.sh
RUN chmod 755 /start.sh
EXPOSE 8080 8088
WORKDIR /opt/In0ri/FlaskApp
CMD ["/start.sh"]
