FROM python:3.8.10

RUN pip install Flask==2.2.0 redis requests

ADD ./genes.py /genes.py

CMD ["python3", "/genes.py"]