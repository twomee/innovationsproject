# first stage
FROM python:3.8 AS builder
WORKDIR /scripts

COPY requirements.txt .

# clean and update sources
RUN apt-get clean && apt-get update

# install dependencies to the local user directory (eg. /root/.local)
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt-get --assume-yes install xclip
RUN pip install --user -r requirements.txt

# second unnamed stage
# FROM python:3.8-slim

# copy only the dependencies installation from the 1st stage image
# COPY --from=builder /root/.local/bin /root/.local
COPY ./scripts .
COPY ./appconfig.ini .

# update PATH environment variable
# ENV PATH=/root/.local/bin:$PATH

CMD [ "python", "./PCTools.py" ]


#how to run docker and apply changes of code:
    #docker stop innovations
    #docker rm innovations
    #docker login -u twome
    #docker pull innovations
    #docker run --publish 8000:8080 --detach --name innovations innovations

#docker run --name mongoDB -d mongo:4.4.0
#docker run -it --network innovations-network --rm mongo mongo --host mongoDB test