FROM python:3
COPY . /usr/src/app
RUN pwd
WORKDIR /usr/src/app 
RUN pip install -r Requirements.txt
CMD ["python3", "-u", "listener.py"]