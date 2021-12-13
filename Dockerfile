# set base image (host OS)
FROM python:3.8-slim

# install sqlite3
RUN apt-get update && apt-get install -y sqlite3

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY pip-modules	 .

# install dependencies
RUN pip install -r pip-modules

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./app.py" ]
