# R Studio

This contains the building blocks to integrate R Studio into our environment

* `rstudio.conf` - an nginx configuratiuon file. It answers /ping request for health checks. It also sends certain URL's to our "front_door" app which authenticates the user and sets an authentication cookie to allow access to RStudio
* `Dockerfile` - An exemplary Dockerfile,  though the base image specifies `rocker/rstudio` we actually take the `rocker/rstudio` image file and append the same commands as the `nginx` Dockerfile and use that as the `BASE_IMAGE`
* `front_door.py` - a simple flask app that responds to health checks and authenticates the user and sets an authentication cookie for RStudio access.
