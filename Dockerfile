# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install the dependencies
RUN pip install  -r requirements.txt 

EXPOSE 8501

# Specify the command to run the application
CMD ["streamlit","run", "gmail_application.py"]