ARG BASE_IMAGE=rocker/rstudio
FROM $BASE_IMAGE

RUN apt-get update && apt-get  install openssl openssh-client ca-certificates libgsl-dev zlib1g-dev --no-install-recommends -y

# LOAD YOUR FAVORITE R MODULES

# We install the following to allow the use of python in R studio
RUN R -e "install.packages('reticulate', repos='http://cran.us.r-project.org')"

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH "/opt/miniconda/bin:$PATH"
RUN pip install boto3 pandas
RUN pip install gunicorn

RUN pip install wheel
RUN pip install setuptools
RUN pip install pycrypto flask python-jose requests
RUN pip install snowflake-connector-python snowflake-sqlalchemy
RUN pip uninstall wheel --yes

ARG RSTUDIO_LOCAL=rstudio
COPY $RSTUDIO_LOCAL/rstudio.conf.template /etc/nginx/conf.d/rstudio.conf
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
RUN apt-get update && apt-get install emacs --no-install-recommends -y

##
## all apt-get must be above this line. The proxy's will kick in after this
## 

ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
ENV http_proxy=http://172.17.0.1:8888/
ENV https_proxy=http://172.17.0.1:8888/
ENV no_proxy=localhost,127.0.0.1,169.254.169.254,169.254.170.2
COPY your_enterprise.crt  /usr/local/share/ca-certificates/
RUN update-ca-certificates

RUN mkdir /usr/local/gateway
COPY $RSTUDIO_LOCAL/front_door.py  /usr/local/gateway/
COPY $RSTUDIO_LOCAL/configure_user.sh /
COPY $RSTUDIO_LOCAL/profile /etc/profile
COPY $RSTUDIO_LOCAL/configure_environment.py /usr/local/bin/

# Patch HMAC.py
ENV PASSWORD="Needed but not used"
ENV RETICULATE_PYTHON /opt/miniconda/bin/python
COPY $RSTUDIO_LOCAL/HMAC.py /opt/miniconda/lib/python3.7/site-packages/Crypto/Hash/
COPY whilabs_tools /opt/miniconda/lib/python3.7/site-packages/whilabs_tools/
CMD "bash"
#CMD ["sh", "/configure_user.sh", "bash"]

