FROM python:3-slim-buster

USER root

ENV APPUSER app_user
# Prepare environment
ENV MY_HOME /opt/app
RUN mkdir -p $MY_HOME
ENV PATH $MY_HOME/bin:$PATH
RUN groupadd --system --gid=9999 ${APPUSER} && \
    useradd --system --home-dir $MY_HOME --uid=9999 --gid=${APPUSER} ${APPUSER}
WORKDIR $MY_HOME



ENV PATH $MY_HOME:/usr/local/bin:$PATH

ADD dist/ServerPingWebSocketPy-0.1.0.tar.gz ${MY_HOME}

WORKDIR $MY_HOME/ServerPingWebSocketPy-0.1.0
RUN chown -R ${APPUSER}:${APPUSER} $MY_HOME
RUN chmod -R 750 $MY_HOME
RUN pip3 install -r requirements.txt

USER app_user


CMD ["./runMktServer.sh"]