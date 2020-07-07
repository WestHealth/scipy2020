# Jupyter Notebook/Lab

We build the docker container based on an established notebook such as base-notebook scipy-notebook tensorflow-notebook
[see github docker-stacks](https://github.com/jupyter/docker-stacks) for example starting docker images

Please note that the files have been modified to remove either sensitive information or code overly custom to our environment so though it should work. It may require some modification for you environment.

The following files are modified:

* `start-notebook.sh` - we modify this to generate a certificate so that when jupyter notebook/lab communicates with the ALB, the communications is encrypted. The certificate can be self-signed.
* `Dockerfile` - An exemplary Dockerfile, you can start from any Jupyter base image you desire
* `login.py` - A modified login file should be placed at `site-packages/notebook/auth/` this validates against the ALB's authentication. `PK_SERVER` and `region` may vary due to your AWS environment
* `logout.py` - Modified to kick you to a `logout_url` environment variable as you may wish to log out of the entire framework not just Jupyter
* `jupyter-notebook-with-shutdown` and `jupyter-lab-with-shutdown` replaces the standard `jupyter-notebook` and `jupyter-lab` replaces the standard  startup scripts and implements self culling. So that when the notebooks/lab shutdown. The service does not restart the container.
