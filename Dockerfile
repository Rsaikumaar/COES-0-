# Use the official Python image as the base image
FROM python:3.11.1

RUN pip install pip
RUN pip install --upgrade pip
# Set the working directory in the container
WORKDIR /COES
RUN apt-get update && apt-get install -y portaudio19-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application files into the working directory
COPY . /COES
# Install the application dependencies
#port 
EXPOSE 5245
# Define the entry point for the container
CMD ["gunicorn", "--bind", "0.0.0.0:5245", "main:app"]
