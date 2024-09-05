################################################################
#
#  Multi staged Dockerfile for Python (micromaamba)
#
#  Contains stages for development and production
#
#  Author: Robert Barachini
#
#  Last updated: 2024-06-09
#
################################################################

################################################################
#  STAGE: 📦 Base image  - Micromamba
################################################################

# https://hub.docker.com/layers/mambaorg/micromamba/latest/images/sha256-5abb59756246288c66e9c9238aa01e749a4be7d5338280a93d9b30cbb633b011
FROM mambaorg/micromamba:latest as base

LABEL maintainer="Robert Barachini"

WORKDIR /usr/src/app

COPY ["./../environment.yml", "./"]

# Renames the environment to base as recommended by micromamba
RUN sed -i 's/^name: .*/name: base/' environment.yml

################################################################
#  STAGE: 🏗️ Build production
################################################################

FROM base as build-production

ENV PYTHON_ENV=production

# Removes the development dependencies from the environment file
# before installing the dependencies
RUN sed -i '/<dev>/d' environment.yml && \
		micromamba install -y -n base -f environment.yml && \
		micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER ./src ./src

################################################################
#  STAGE: 🏗️ Build development
################################################################

FROM base as build-development

ENV PYTHON_ENV=development

RUN micromamba install -y -n base -f environment.yml && \
		micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER ./src ./src

################################################################
#  STAGE: ⚙️ Run development
################################################################

FROM build-development as development

ENV PYTHON_ENV=development

USER $MAMBA_USER

EXPOSE 5678

# CMD python src/sample.py
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client src/sample.py

################################################################
#  STAGE: ⚙️ Run production
################################################################

FROM build-production as production

ENV PYTHON_ENV=production

USER $MAMBA_USER

CMD ["python", "src/sample.py"]