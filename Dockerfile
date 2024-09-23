FROM python:3.11

WORKDIR /code

RUN apt update && apt install -y cron && apt instal -y vim

COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN chmod 0644 /etc/cron.d/ml-work-cronjob

COPY src/mnist/ /code/

COPY run.sh /code/run.sh
RUN chmod +x /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/Jeonghoon2/mnist.git@0.3/worker

CMD ["sh", "run.sh"]