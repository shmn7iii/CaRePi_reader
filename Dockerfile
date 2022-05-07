FROM python:3
USER root

RUN apt-get update \
  && pip install --upgrade pip \
  && pip install --upgrade setuptools

WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

CMD ["python" "main.py"]
