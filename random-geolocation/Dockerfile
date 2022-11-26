# FROM python:3.9.13-slim


# # Install GDAL dependencies
# RUN apt-get -y update && \
#     apt-get install -y libgdal-dev g++ --no-install-recommends && \
#     apt-get clean -y

# # Update C env vars so compiler can find gdal
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal

# WORKDIR /app

# COPY ./pyproject.toml /app 

# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
# RUN pip3 install poetry &&\ 
#     poetry config virtualenvs.create false &&\ 
#     poetry install --only main

# COPY ./random_geolocation /app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


# 
FROM python:3.9.13-slim as requirements-stage

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.9.13-slim

# 
WORKDIR /code

# 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./random_geolocation /code/app

# 
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
