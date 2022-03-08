#!/usr/bin/env python3

import cherrypy
import os

class app():
    
    @cherrypy.expose
    def index(self):
        return open("thing.html")

if __name__ == "__main__":

    application = app()

    ABSPATH = os.path.abspath(os.getcwd())

    injectedConfig = dict()

    injectedConfig["/"] = { "tools.staticdir.on": True, "tools.staticdir.dir": ABSPATH }

    cherrypy.quickstart(application, "/", injectedConfig)
