FROM ubuntu:20.04
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN groupadd --gid 1000 hints && \
    useradd -ms /bin/bash --gid 1000 --uid 1000 hints && \
    apt-get update && \
    apt-get install -y python3 python3-pip vim && \
    pip3 install --upgrade pip six setuptools
USER hints
COPY app /home/hints/app
WORKDIR /home/hints/app
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]