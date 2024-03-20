FROM ubuntu

WORKDIR /app
ADD . /app

RUN apt update
RUN apt install python3 -y
RUN apt install pip -y
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt install ffmpeg -y


EXPOSE 80

CMD ["python3", "app.py"]
