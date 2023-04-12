FROM python:3.8.10

RUN pip install Flask==2.2.0 redis requests imgur-python==0.2.4 matplotlib==3.7.1

ADD ./genes.py /genes.py

CMD ["python3", "/genes.py"]