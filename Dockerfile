FROM python:3.11

WORKDIR /code

RUN apt update && apt install -y cron && apt install -y vim

COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/ /code/

COPY run.sh /code/run.sh
RUN chmod +x /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/Jeonghoon2/mnist.git@main

CMD ["sh", "run.sh"]