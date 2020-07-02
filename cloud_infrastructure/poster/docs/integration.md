---
no_toc: True
slim: True
---
# Authentication and Applications

![Shared Authentication](authentication.svg)

Securing the environment so that only authorized users have access to their own container environments are a shared responsibility between the Identity Provider (IDP), Application Load Balancer (ALB) and the end application. Following these guidelines mitigates vulnerabilities due to misconfiguration such as a validated user being able to access another user's protected resources.

## Authentication Responsibility

  * IDP
      -  authenticates user
  * ALB
      - authenticates user via IDP over [OIDC](OpenId Connect)
      - provides JWT token to application via the `x-amzn-oidc-data` header
      - JWT token provides the user identity
  * Application
      - provide health check url
      - validates JWT token and extracts user identity
      - verifies access to resources (e.g. shared drives) is permitted by specified user.

Specifics are described in greater detail in the companion proceedings article and in the examples for specific applications.

  * [Jupyter](jupyter.md)
  * [Rstudio](rstudio.md)
  * [Desktop App Via VNC](novnc.md)
  * [Custom Applications](#custom-applications)
  * [Apache Superset](#apache-superset)

## Custom Applications

In developing your own bespoke applications, a layer of authentication
can be employed. In consideration of developing or adapting your own
application, you should provide an unauthenticated URL for the ALB's
health check and be equipped to configure the base URL. Authentication
can be easily plugged into most web server frameworks.

A `@login_required` decorator is provided in the code [here]()


## Apache Superset

Apache Superset has become an increasingly important business intelligence tool for the data scientist. Though we have not adapted it to this infrastructure yet, cursory readings of the documentation indicates that custom python authenticator can be used. Since Superset has user management built in, the custom authenticator should integrate with the user management.