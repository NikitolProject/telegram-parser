FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system app && adduser app app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./static/. $HOME/static
RUN pip install -r requirements.txt

## copy project
#COPY . $APP_HOME
#
## chown all the files to the app user
#RUN chown -R app:app $APP_HOME
#
## change to the app user
#USER app

# run entrypoint.prod.sh
#ENTRYPOINT ["/home/app/web/entrypoint.sh"]
