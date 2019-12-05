ARG SERVER_IMAGE=registry.gitlab.nglm.rt.ru/nglm/smtpapi/smtpapi

FROM ${SERVER_IMAGE}:latest
ARG TZ
ARG CONFIG


RUN cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone

# Add source code
RUN rm -rf /app
COPY smtpapi /app
COPY ${CONFIG} /app/config.yml
CMD ["gunicorn", "-w 3", "-b :8080", "api:app"]
