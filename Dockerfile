FROM python:alpine3.10 as build-env

USER root

ENV APPUSER app_user
# Prepare environment
ENV MY_HOME /opt/app
RUN mkdir -p $MY_HOME

ENV LD_LIBRARY_PATH /lib64
RUN apk add --update libc6-compat
RUN apk add --virtual build-dependencies \
        build-base \
        gcc
ENV SOFTWARE_PATH build/distributions/
RUN addgroup -S $APPUSER && adduser -D -S -H -G $APPUSER -h $MY_HOME $APPUSER
WORKDIR $MY_HOME

ENV PATH $MY_HOME:/usr/local/bin:$PATH

ADD dist/ServerPingWebSocketPy-0.1.0.tar.gz ${MY_HOME}

ENV APPDIR $MY_HOME/ServerPingWebSocketPy-0.1.0
WORKDIR $APPDIR
RUN chown -R ${APPUSER}:${APPUSER} $APPDIR
RUN chmod -R 750 $APPDIR
RUN pip3 install -t $APPDIR -r requirements.txt

USER app_user

FROM python:alpine3.10

ENV APPUSER app_user
# Prepare environment
ENV MY_HOME /opt/app
RUN mkdir -p $MY_HOME

ENV LD_LIBRARY_PATH /lib64
RUN apk add --update libc6-compat

RUN addgroup -S $APPUSER && adduser -D -S -H -G $APPUSER -h $MY_HOME $APPUSER
WORKDIR $MY_HOME

ENV PATH $MY_HOME:/usr/local/bin:$PATH

ENV APPDIR $MY_HOME/ServerPingWebSocketPy-0.1.0
WORKDIR $APPDIR

COPY --from=build-env $APPDIR $APPDIR
RUN chown -R $APPUSER $MY_HOME

ENV PYTHONPATH $APPDIR

CMD ["sh", "runMktServer.sh"]