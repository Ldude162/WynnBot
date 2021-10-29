FROM python:3
COPY bot.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN --mount=type=secret,id=TESTING_TOKEN \
    --mount=type=secret,id=DISCORD_TOKEN \
    export DISCORD_TOKEN=$(cat /run/secrets/DISCORD_TOKEN) && \
    export TESTING_TOKEN=$(cat /run/secrets/TESTING_TOKEN) && \
    yarn gen
CMD python bot.py
