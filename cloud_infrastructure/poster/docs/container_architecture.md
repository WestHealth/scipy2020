---
no_toc: True
slim: True
---
# Container Architecture

![Cloud Architecture. cloudfig](container.svg)

## Hub Container

   * Prompts an unauthenticated user for authenticatin
   * Allocates resources when an unresourced user/application is requested
   * Insures the ECS service associated with a user/application
   * Grants permissions via a role so that the container has proper rights
      - Boundary permissions are imposed on the hub container to prevent escalation of permissions should the hub become compromised

## Provisioner Container

   * Lightweight task that mounts the shared drive and ensures all drives and directories require exist
   * Separate from Hub for security
      - Hub has no access to shared drive
      - Provisioner has no extraordinary access rights
   * Provisioner ensures permissions on shared drive are correct
   * Provisioner container is ephermeral

## Application Containers

   * Can have many flavors see this [panel](integration.md)
   * Is responsible for confirming the user's identity through ALB authentication
   * Can self cull inactive containers (e.g., Jupyter)

Modification to Jupyter's startup script for notebook and labs can be found [here](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/jupyter). Cloudformation templates managing the [hub](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/hub/hub.yaml) and [applications](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/hub/notebook.yaml) are also provided.


