#FROM jupyter/base-notebook
#FROM jupyter/scipy-notebook
# We make the base image configurable.
ARG BASE_IMAGE=jupyter/tensorflow-notebook
FROM $BASE_IMAGE
USER root
RUN apt update
RUN apt install git openssh-client -y
RUN conda update -n base conda
# INSTALL YOUR FAVORIATE CONDA PACKAGES HERE
#
RUN chown -R $NB_USER /opt/conda/pkgs
RUN mkdir /usr/local/gateway
RUN mkdir /usr/share/notebook
RUN chown $NB_USER /usr/share/notebook
# We put all the modified files in a subdirectory LOCAL_JUPYTER
# Since the conda solution has caused us to back track python versions, we just install copies of our code into all version
ARG LOCAL_JUPYTER=jupyter
COPY $LOCAL_JUPYTER/logout.py $LOCAL_JUPYTER/login.py /opt/conda/lib/python3.7/site-packages/notebook/auth/
COPY $LOCAL_JUPYTER/login.html /opt/conda/lib/python3.7/site-packages/notebook/templates/
COPY $LOCAL_JUPYTER/logout.py $LOCAL_JUPYTER/login.py /opt/conda/lib/python3.6/site-packages/notebook/auth/
COPY $LOCAL_JUPYTER/login.html /opt/conda/lib/python3.6/site-packages/notebook/templates/
RUN chown $NB_USER /usr/local/gateway
COPY $LOCAL_JUPYTER/start-notebook.sh /usr/local/bin/
COPY $LOCAL_JUPYTER/jupyter-notebook-with-shutdown $LOCAL_JUPYTER/jupyter-lab-with-shutdown  /opt/conda/bin/
RUN chmod 755 /usr/local/bin/configure_user /opt/conda/bin/jupyter-notebook-with-shutdown /opt/conda/bin/jupyter-lab-with-shutdown
WORKDIR /home/$NB_USER
# Optionally clean the installed cache to make the end image smaller
RUN rm -rf /home/$NB_USER/.cache/*

# The following is for using the proxy for the container. The firewall may require a trusted_enterprise certificate
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
ENV http_proxy=http://172.17.0.1:8888/
ENV https_proxy=http://172.17.0.1:8888/
ENV no_proxy=localhost,127.0.0.1,169.254.169.254,169.254.170.2
COPY trusted_enterprise.crt  /usr/local/share/ca-certificates/
RUN update-ca-certificates
