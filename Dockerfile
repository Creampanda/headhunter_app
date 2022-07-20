FROM ubuntu:20.04
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN groupadd --gid 1000 hints && \
    useradd -ms /bin/bash --gid 1000 --uid 1000 hints && \
    apt-get update && \
    apt-get install -y python3 python3-pip vim supervisor && \
    pip3 install --upgrade pip six setuptools 
USER hints
WORKDIR /home/hints
COPY --chown=hints:users app /home/hints/app
RUN mkdir -p ./log/supervisor && python3 -m pip install -r ./app/requirements.txt
COPY --chown=hints:users ./supervisor_tasks.conf ./supervisor_tasks.conf
ENTRYPOINT ["supervisord", "--nodaemon", "-c", "./supervisor_tasks.conf"]