FROM 10.29.6.41/registry/containers/ubi-with-python/ubi8
ARG PROXY_USER
ARG PROXY_PASSWORD
ARG PROXY_HOST
ARG PROXY_STRING=http://$PROXY_USER:$PROXY_PASSWORD@$PROXY_HOST

ENV HTTPS_PROXY=${PROXY_STRING} \
    http_proxy=${PROXY_STRING} \
    https_proxy=${PROXY_STRING} \
    HTTP_PROXY=${PROXY_STRING} \
    PIP_TRUSTED_HOST="pypi.python.org pypi.org files.pythonhosted.org"

RUN echo "[main]" >> /etc/dnf/dnf.conf && \
    echo "gpgcheck=1" >> /etc/dnf/dnf.conf && \
    echo "installonly_limit=3" >> /etc/dnf/dnf.conf && \
    echo "clean_requirements_on_remove=True" >> /etc/dnf/dnf.conf && \
    echo "best=True" >> /etc/dnf/dnf.conf && \
    echo "sslverify=False" >> /etc/dnf/dnf.conf && \
    echo "proxy=http://$PROXY_HOST" >> /etc/dnf/dnf.conf && \
    echo "proxy_username=$PROXY_USER" >> /etc/dnf/dnf.conf && \
    echo "proxy_password=$PROXY_PASSWORD" >> /etc/dnf/dnf.conf && \
    echo "proxy_auth_method=basic" >> /etc/dnf/dnf.conf

# Update image and install python
RUN dnf update && \
    dnf install -y python36

#Add source code
COPY /smtpapi /app
COPY config.prod.yml /app/config.yml
COPY requirements.txt /app/requirements.txt
WORKDIR /app

#Install requirements \
RUN pip3 install -r requirements.txt

RUN dnf clean all && \
rm -rf /etc/dnf/dnf.conf && \
unset HTTPS_PROXY http_proxy https_proxy HTTP_PROXY

#Expose port gunicorn \
EXPOSE 8080

# Command for start gunicorn server
# -w --workers
# -b port and ip adress
# here you need use your main file
# for exmaple if file api.py you need use api:app
CMD ["gunicorn", "-w 3", "-b :8080", "api:app"]