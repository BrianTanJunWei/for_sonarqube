# Use the official Jenkins image as the base image
FROM jenkins/jenkins:lts AS jenkins

# Switch to the root user to install additional tools
USER root

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
# Create a virtual environment
RUN python3 -m venv /opt/venv
# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements.txt from the 'backend' directory to the root of the image
COPY requirements.txt /

# Install Python packages from requirements.txt
RUN pip install -r /requirements.txt

USER jenkins

