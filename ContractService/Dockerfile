FROM python:3
COPY . /usr/src/app
RUN pwd
WORKDIR /usr/src/app
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r Requirements.txt
CMD ["python3", "AssetTrackerService.py"]