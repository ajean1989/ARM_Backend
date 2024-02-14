FROM python:3.11

WORKDIR /init

COPY ./tests ./tests

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./tests/requirements.txt
# CMD ["sleep", "infinity"]
CMD ["python", "-m",  "pytest",  "-sv"] 



