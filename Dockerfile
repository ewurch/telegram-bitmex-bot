FROM python:3.6
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python", "./twitter_scrapper.py"]
