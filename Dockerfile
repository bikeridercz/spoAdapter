# set base image (host OS)
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY pip-module-list .

# install dependencies
RUN pip install -r pip-module-list

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./app.py" ]
