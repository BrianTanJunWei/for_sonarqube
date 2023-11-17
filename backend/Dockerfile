FROM python:3.9

# Set the working directory and grant permissions to the new user
WORKDIR /backend

# Copy your application code
COPY . .

# Expose the necessary port
EXPOSE 5000

# Install the application's dependencies
RUN pip install -r requirements.txt
