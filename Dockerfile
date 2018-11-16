FROM python:3.6
  
ADD /coe332-kn7854/compiled /
ADD /coe332-kn7854/hw8 /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD ["python", "api.py"]
