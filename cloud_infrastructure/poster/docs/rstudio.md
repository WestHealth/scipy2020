---
no_toc: True
slim: True
---
# RStudio

![Inside the RStudio Container rstudio](rstudio.svg)

Our implementation of RStudio Server on the same cloud platform is
non-invasive to the code base, but more complicated architecturally.

The container is made up of three components, a proxy, RStudio server, and a custom app. A dockerfile is available [here](broken link)

#### The proxy

  * Separates traffic destined for the custom app and RStudio server
  * Rewrites the url on traffic destined for RStudio server stripping off the base_url
  * Uses a certificate to so all extra-container communications is over HTTPS
  
#### Custom App

  * Source code is available [here](broken link)
  * Fields `/ping` request for the internal health check
  * Captures the `auth-sign-in` URL and authenticates and verifies user identity
  * Sets authentication cookie for RStudio server

#### Rstudio Server

  * No customization is required.

Return to [Authentication and Applications](integration.md)