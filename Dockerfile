# Use the official Python image as the base image
FROM python:3.11.1

RUN pip install --no-cache-dir pip==23.1.2
# Set the working directory in the container
WORKDIR /COES

# Copy the application files into the working directory
COPY . /COES

# Install the application dependencies
RUN pip install -r requirements.txt
#port 
EXPOSE 8888
# Define the entry point for the container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
