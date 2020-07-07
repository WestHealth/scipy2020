#!/bin/bash
set -e

openssl req -config /etc/ssl/openssl.cnf -x509 -nodes -days 365 -newkey rsa:2048 -keyout /usr/share/notebook/notebook.key -out /usr/share/notebook/notebook.pem -subj "/"
if [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
  . /usr/local/bin/start.sh jupyter lab-with-shutdown "$@" --certfile=/usr/share/notebook/notebook.pem --keyfile /usr/share/notebook/notebook.key 
else
  . /usr/local/bin/start.sh jupyter notebook-with-shutdown "$@" --certfile=/usr/share/notebook/notebook.pem --keyfile /usr/share/notebook/notebook.key
fi
