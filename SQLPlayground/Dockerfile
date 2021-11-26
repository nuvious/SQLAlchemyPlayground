from python:3.9-bullseye

COPY . /app
WORKDIR /app
RUN ls -al
RUN pip install -r requirements.txt
CMD /bin/bash run_playground.sh
