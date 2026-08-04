# Use an official Python runtime as a parent image
FROM python:3.8.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y libssl-dev libffi-dev
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run python script when the container launches
# CMD ["python", "./main.py"]
CMD ["tail", "-f", "/dev/null"]