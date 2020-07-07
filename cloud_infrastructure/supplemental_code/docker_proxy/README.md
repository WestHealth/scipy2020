# Proxy Environment Variables set via Dockerfile

Add the lines in `Dockerfile` to your Dockerfile to set environment variables to configure the http proxy for a container. However, add them after any network related commands in your build such as apt-get otherwise your container won't build.
