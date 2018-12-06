FROM python:3.6

RUN pip install -r requirements.txt

ADD ./source /source
WORKDIR /source

ENTRYPOINT ["python"]
CMD ["api.py"]
