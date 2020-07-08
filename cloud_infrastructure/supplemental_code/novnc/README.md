# VNC server with webVNC client

We use [novnc](https://github.com/novnc/noVNC) and [websockify](https://github.com/novnc/websockify)
as a client and [tigerVNC](https://github.com/TigerVNC/tigervnc) as a server. We modeled our Dockerfile on the one supplied by [headless-vnc](https://github.com/ConSol/docker-headless-vnc-container) though it does not appear to be maintained.

The main modified files are

   * `vnc_lite.html` - we modified to use the `BASE_URL` and the `VNC_PW` set in the environment
   * `auth_plugins.py` - We added the plugin `AmazonAuth` your `PK_SERVER` and `region` may differ based on your AWS environment
   * `customrequesthandler.py` - replaces the `bSimpleHTTPRequestHandler` from `SimpleHTTPServer` used by `websockifyserver.py`
      - supports a `/ping` path for health checks
      - implements a `BASE_URL`
      - implements a rudimentary templating framework to allow customization of `vnc_lite.html`
   * `websockifyserver.py` - modify `WebSockifyRequestHandler` to subclass `CustomRequestHandler` instead of `SimpleHTTPRequestHandler` remove `do_GET` as it is customized in  `CustomRequestHandler`
