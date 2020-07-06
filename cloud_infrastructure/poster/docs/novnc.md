---
no_toc: True
slim: True
---
# Virtual Network Computing (VNC) Containers

![Inside a VNC Container](novnc.svg)

This uses a headless VNC container. It contains three major components,
a headless VNC client, a VNC server and the end application running on the underlying operating system.

#### noVNC

   * headless VNC client servers as a web to vnc proxy.
   * responsible for authenticating HTTPS and websocket connection
   * connects to VNC server through a port that is not exposed outside the container
   * authentication added to [websockifyproxy.py](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/novnc/websockifyproxy.py)

#### VNC
   * allows access from noVNC client to any underlying operation
   * turns the container into a virtual computer
   * requires a password, but exposure of password does not compromise the system

#### End Application
   * No customization required
   * Data applications include Orange and Falcon

Return to [Authentication and Applications](integration.md)