ARG SERVER_IMAGE

FROM ${SERVER_IMAGE}:latest
ARG TZ
ARG CONFIG


RUN cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone

# Add source code
COPY smtpapi /app
COPY ${CONFIG} /app/config.yml
CMD ["gunicorn", "-w 3", "-b :8080", "api:app"]
