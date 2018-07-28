"""
Created on Jul 31, 2014

@author: ionut
"""

import datetime
import json
import logging
import tornado.ioloop
import tornado.web
import pymongo

import settings
from utils import gps_to_json

logging.basicConfig(level=settings.LOG_LEVEL, datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] - %(levelname)s - %(message)s")


class BaseHandler(tornado.web.RequestHandler):
    """
    Main handler to be be inherited by subsequent handlers
    """


    def initialize(self):
        self.database = self.settings["database"]
        self.secret = self.settings["secret"]


    @tornado.web.asynchronous
    def get(self):
        self.render("home.html")


    def post(self):
        self.finish("POST not allowed")


class UploadHandler(BaseHandler):
    """
    Upload handler to receive and process data from bbgps application
    """


    @tornado.web.asynchronous
    def post(self):
        data = self.request.arguments
        if not data:
            return self.finish("include position data")

        if data["secret"] != self.secret:
            return self.finish("invalid authentication")

        position = {}
        position["bearing"] = float(data["bearing"][0])
        position["battlevel"] = int(data["battlevel"][0])
        position["altitude"] = float(data["altitude"][0])
        position["provider"] = data["provider"][0]
        position["time"] = datetime.datetime.strptime(data["time"][0], "%Y-%m-%dT%H:%M:%S.%fZ")
        position["latitude"] = float(data["latitude"][0])
        position["longitude"] = float(data["longitude"][0])
        position["speed"] = float(data["speed"][0])
        position["charging"] = int(data["charging"][0])
        position["accuracy"] = float(data["accuracy"][0])

        self.application.cache["last_pos"] = [position]
        self.database.positions.insert(position)
        logging.info("received %s", json.dumps(position))
        self.finish(json.dumps({"status": "OK"}))


    def get(self):
        self.finish("GET not allowed")


class WebHandler(BaseHandler):
    """
    Retrieve position data (live or history)
    """


    @tornado.web.asynchronous
    def get(self, op):
        if op == "history":
            pos = self.database.positions.find({}, {"_id" : 0}).sort([("_id", 1)]).limit(8192)
        elif op == "now":
            if not self.application.cache.get("last_pos"):
                pos = self.database.positions.find({}, {"_id" : 0}).sort([("_id", -1)]).limit(1)
                self.application.cache["last_pos"] = list(pos)
            pos = self.application.cache["last_pos"]
        else:
            pos = []
        data = gps_to_json(list(pos))
        self.finish(data)


    def post(self):
        self.finish("POST not allowed")


def main():
    """
    Create database connection, Tornado application instance and start ioloop
    """
    conn = pymongo.MongoClient(settings.DB_URI)
    database = conn[settings.DB_NAME]

    application = tornado.web.Application(
        [
            (r"/", BaseHandler),
            (r"/upload", UploadHandler),
            (r"/web/([^/]+)", WebHandler),
        ],
        database=database, secret=settings.SECRET, debug=settings.DEBUG, gzip=True,
        template_path=settings.TEMPLATE_PATH,
        static_path=settings.STATIC_PATH
    )
    application.cache = {}

    logging.info("starting bbgps...")
    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
