#!/usr/bin/env python3
from flup.server.fcgi import WSGIServer
from api import make_app

if __name__ == "__main__":
    application = make_app()
    WSGIServer(application).run()
