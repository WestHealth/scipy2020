# Our Hub

This contains the building blocks to show how our hub authenticates and the cloudformation templates used to build containers in our environment

* `front_door.py` - a simple flask app that responds to health checks and authenticates the user. It puts up a welcome page if authenticated, a single page with a login button if not authenticated. The login action sends the user to a URL which causes the ALB to authenticate.
* `hub.yaml` - the cloudformation template to spawn a service related to the hub container. It also imposes a boundary permission, so that if somehow the hub is compromised, the amount of escalation possible is severely limited
* `notebook.yaml` - perhaps a misnomer, this cloudformation template is used to spin up a service for any application in our ecosystem. The type of application is dependent on the docker image defined.
