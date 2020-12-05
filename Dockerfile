FROM python:3.7-alpine
MAINTAINER EgorSemenov "wildworld2727@tut.by"
WORKDIR /usr/src/app
RUN apk add --no-cache git && \
    git clone https://github.com/EgorSemenov/FifaPortal.git
WORKDIR /usr/src/app/FifaPortal
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD [ "fifaportal.py" ]