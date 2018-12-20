FROM golang:1.11.3-stretch

# From the repository root, run
# docker build -f Dataset/Dockerfile -t openschemas/extractors:Dataset .

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

LABEL "com.github.actions.name"="Dataset Extractor"
LABEL "com.github.actions.description"="Extract schema.org Dataset for Dockerfile"
LABEL "com.github.actions.icon"="cloud"
LABEL "com.github.actions.color"="blue"

LABEL "repository"="https://www.github.com/openschemas/extractors"
LABEL "homepage"="https://www.github.com/openschemas/extractors"
LABEL "maintainer"="Vanessa Sochat <vsochat@stanford.edu>"

# Add local files
ADD . /code

WORKDIR /code/Dataset

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install --upgrade pip && \
    pip install spython && \
    pip install openschemas && \
    pip install schemaorg && \
    chmod u+x /code/Dataset/entrypoint.sh && \
    chmod u+x /code/Dataset/deploy.sh

ENTRYPOINT ["/bin/bash", "/code/Dataset/entrypoint.sh"]
