FROM ubuntu:20.04
COPY bot.py .
RUN python bot.py
