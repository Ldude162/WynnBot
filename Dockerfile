FROM python:3
COPY bot.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG TESTING_TOKEN
ARG DISCORD_TOKEN
ENV TESTING_TOKEN=$TESTING_TOKEN
ENV DISCORD_TOKEN=$DISCORD_TOKEN
CMD echo $TESTING_TOKEN
CMD echo $DISCORD_TOKEN
CMD python bot.py
