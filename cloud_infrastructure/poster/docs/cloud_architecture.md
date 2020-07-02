---
no_toc: True
slim: True
---
# Cloud Architecture

![Cloud Architecture](cloud.svg)

The basic components in our cloud architecture are:

   * Identity provider (IDP) used to authenticate a user
   * Application load balancer (ALB) to load balance, route and regulate user access through authentication
   * A cluster of elastic cloud computer compute (EC2) instances to instantiate
the containers
   * ECS Cluster to manage containers
cluster.

#### ECS Specifics

   * task definitions used to configure container environement
      - one container per application
      - depending on application type one per user if application doesn't have adequate user management
   * ECS Services automate management of resources associated with each task
      - container port mapping
      - health checks
      - target groups for the ALB

#### ALB Specifics

   * ALB performs authentication through OpenID Connect (OIDC)
   * Recommend enforcement of HTTPS for encryption in transit
   * Use listener rules and path and/or hostname routing to route to different containers under the same domain
   * Recommend ALB connect to application via HTTPS to ensure encryption is end to end

#### Shared Storage

   * ObjectiveFS or Elastic File System (EFS) can be used
   * Ensure file system is encrypted
   * Ensure network mounted drives use encrypted communications

#### Other Resources

   * CloudWatch to monitor logs from inside each container
   * IAM roles to manage access permissions
   * Cloudformation enables easier management of AWS resources for associated with each container

