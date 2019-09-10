FROM python:latest
COPY . /twitter_app
WORKDIR /twitter_app
RUN pip install -r requirements.txt
CMD python ./twitter_scrape.py
