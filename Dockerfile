FROM python:3.10.4

RUN apt-get update \
  && apt-get upgrade -y \
  && pip install --upgrade pip

WORKDIR /carepi

COPY . /carepi

RUN pip install requirements.txt

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

CMD ["python" "main.py"]
