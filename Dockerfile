FROM python:3.8.10

# optional labels to provide metadata for the Docker image
# (source: address to the repository, description: human-readable description)
LABEL org.opencontainers.image.source https://github.com/mehdiattar-lab/NIS.git
LABEL org.opencontainers.image.description "Docker image for the network information system (NIS) component."

# create the required directories inside the Docker image
#
# the NIS component has its own code in the NIS
# directory and it uses code from the init, simulation-tools and domain-tools directories
# the logs directory is created for the logging output

RUN mkdir -p /NIS
RUN mkdir -p /init
RUN mkdir -p /logs
RUN mkdir -p /simulation-tools
RUN mkdir -p /domain-tools

# install the python libraries inside the Docker image

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# copy the required directories with their content to the Docker image

COPY NIS/ /NIS/
COPY init/ /init/
COPY simulation-tools/ /simulation-tools/
COPY domain-tools/ /domain-tools/

# set the working directory inside the Docker image
WORKDIR /

# start command that is run when a Docker container using the image is started
#
# in this case, "component" module in the "NIS" directory is started

CMD [ "python3", "-u", "-m", "NIS.component" ]