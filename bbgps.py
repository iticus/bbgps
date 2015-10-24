'''
Created on Jul 31, 2014

@author: ionut
'''

import datetime
import json
import logging
import settings
import pymongo
import tornado.ioloop
import tornado.web
from utils import gps_to_json

logging.basicConfig(level=settings.LOG_LEVEL, #filename='bbgps.log', 
    format='[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class BaseHandler(tornado.web.RequestHandler):
    
    def initialize(self):
        self.database = self.settings['database']
        self.secret = self.settings['secret']
    
    @tornado.web.asynchronous
    def get(self):
        self.render('home.html')
    
    def post(self):
        self.finish('POST not allowed') 


class UploadHandler(BaseHandler):
    
    @tornado.web.asynchronous
    def post(self):
        data = self.request.arguments
        if not data:
            return self.finish("include position data")
        
        if data['secret'] != self.secret:
            return self.finish('invalid authentication')
            
        position = {}
        position['bearing'] = float(data['bearing'][0])
        position['battlevel'] = int(data['battlevel'][0])
        position['altitude'] = float(data['altitude'][0])
        position['provider'] = data['provider'][0]
        position['time'] = datetime.datetime.strptime(data['time'][0], '%Y-%m-%dT%H:%M:%S.%fZ')
        position['latitude'] = float(data['latitude'][0])
        position['longitude'] = float(data['longitude'][0])
        position['speed'] = float(data['speed'][0])
        position['charging'] = int(data['charging'][0])
        position['accuracy'] = float(data['accuracy'][0])
        
        self.database.positions.insert(position)
        logging.info('received %s' % json.dumps(position))
        self.finish(json.dumps({'status': 'OK'}))
    
    def get(self):
        self.finish('GET not allowed')


class WebHandler(BaseHandler):
    
    @tornado.web.asynchronous
    def get(self, op):
        if op == 'history':
            positions = list(self.database.positions.find({}, {"_id" : 0}).sort([('_id', -1)]).limit(8192))
            positions.reverse()
        elif op == 'now':
            positions = self.database.positions.find({}, {'_id' : 0}).sort([('_id', -1)]).limit(1)
        else:
            positions = []
        data = gps_to_json(positions)
        self.finish(data)
    
    def post(self):
        self.finish('POST not allowed')


if __name__ == "__main__":
    
    conn = pymongo.MongoClient(settings.DB_URI)
    db = conn[settings.DB_NAME]
    
    application = tornado.web.Application([
        (r"/", BaseHandler),
        (r"/upload", UploadHandler),
        (r"/web/([^/]+)", WebHandler),
    ], database=db, secret=settings.SECRET, debug=settings.DEBUG, gzip=True,
    template_path=settings.TEMPLATE_PATH,
    static_path=settings.STATIC_PATH)
    
    logging.info('starting bbgps...')
    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
