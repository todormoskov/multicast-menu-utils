FROM python:3.9.13
ENV PYTHONUNBUFFERED=1
WORKDIR /multicast
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# RUN apt-get update && apt-get install -y software-properties-common
# RUN add-apt-repository -y ppa:videolan/master-daily
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 09589874801DF724
# RUN apt-get update && apt-get install -y vlc
