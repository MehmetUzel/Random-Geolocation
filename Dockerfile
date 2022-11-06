FROM python:3.10.5-slim-buster

WORKDIR /app_demo

# Install GDAL dependencies
RUN apt-get -y update && \
    apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]

# FROM python:3.9.13-slim

# COPY /watchdog_service /app
# COPY pyproject.toml /app 
# WORKDIR /app
# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
# RUN pip3 install poetry &&\ 
#     poetry config virtualenvs.create false &&\ 
#     poetry install --no-dev

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]