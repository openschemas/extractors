FROM golang:1.11.3-stretch

# docker build -t openschemas/extractors-imagedefinition .

################################################################################
#
# Copyright (C) 2018 Vanessa Sochat.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

RUN apt-get update && \
    apt-get install -y automake \
                       libffi-dev \ 
                       libxml2 \
                       libxml2-dev \
                       libxslt-dev \
                       libxslt1-dev \
                       git \
                       gcc g++ \
                       python3-dev \
                       python3 \
                       wget \
                       locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
ENV MESSAGELEVEL QUIET

LABEL Maintainer vsochat@stanford.edu

# Install container-diff from master
RUN go get github.com/GoogleContainerTools/container-diff && \
    cd ${GOPATH}/src/github.com/GoogleContainerTools/container-diff && \
    go get && \
    make && \
    go install && \
    mkdir -p /code && \
    apt-get autoremove

# Add local files
ADD . /code

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install --upgrade pip && \
    pip install spython && \
    pip install openschemas && \
    pip install schemaorg && \
    chmod u+x /code/entrypoint.sh && \
    mkdir -p /root/.docker && \
    echo {} > /root/.docker/config.json

WORKDIR /code
ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]
