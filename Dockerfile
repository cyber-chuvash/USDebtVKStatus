FROM python:3.7-stretch
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
RUN dpkg-reconfigure --frontend=noninteractive locales
COPY Pipfile.lock /Pipfile.lock
COPY Pipfile /Pipfile
RUN pip install pipenv
RUN pipenv install --system
COPY run.py /app/
COPY config.py /app/
WORKDIR /app
CMD ["python3", "run.py"]
