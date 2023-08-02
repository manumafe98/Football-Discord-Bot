FROM python:3.11

# Set environment variables
ENV API_KEY test
ENV BOT_TOKEN test

# Create the workdir
WORKDIR /bot

# Copy the bot to the workdir
COPY . /bot

# Install the app requirements
RUN pip install -r requirements.txt

# Initialize the bot
CMD python football_bot.py