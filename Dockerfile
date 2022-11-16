FROM python:3.9-slim

COPY . /root

WORKDIR /root
# поменять на requirements
RUN pip install -r requirements.txt