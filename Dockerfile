FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob

COPY src/mnist/ /code/
COPY run.sh /code/run.sh
RUN chmod +x /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/Jeonghoon2/mnist.git@0.3/worker

CMD ["sh", "run.sh"]