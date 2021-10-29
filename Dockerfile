FROM python:3
COPY bot.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG TESTING
ARG DISCORD
ENV TESTING_TOKEN=$TESTING
ENV DISCORD_TOKEN=$DISCORD
CMD python bot.py
