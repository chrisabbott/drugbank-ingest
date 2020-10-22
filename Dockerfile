FROM python:3.9

WORKDIR /project

# Install Chrome and chromedriver (used for rendering JS in Scraper.py)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set a display port to make chromedriver happy
ENV DISPLAY=:99

# Install and configure postgres and create db
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y postgresql postgresql-client postgresql-contrib

USER postgres

RUN /etc/init.d/postgresql start && \
    psql --command "ALTER USER postgres PASSWORD 'postgres';" && \
    createdb drugbank-postgres

# Install all requirements for scraper
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD [ "./run.sh" ]
