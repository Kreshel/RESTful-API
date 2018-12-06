FROM python:3.6

ADD ./source /source
WORKDIR /source

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["api.py"]