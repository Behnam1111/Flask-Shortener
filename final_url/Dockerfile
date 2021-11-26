FROM python:stretch

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN mkdir /usr/src/final_url

WORKDIR /usr/src/final_url

COPY ./fus_url/requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["gunicorn", "-w", "4", "fus_url.app:app"]
