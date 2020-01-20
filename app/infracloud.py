import falcon
import redis
from random import randint
from werkzeug.serving import run_simple
import ujson
from configparser import ConfigParser

class Url():

    def on_get(self, req, resp):
        config = ConfigParser()
        config.read('config.ini')
        req_params = req.params
        conn = redis.Redis(config.get('redis', 'host'),db=3)
        original_url = conn.get(req_params["short_url"])
        resp_json = {}
        resp_json["original_url"] = original_url
        resp_json = ujson.dumps(resp_json)
        resp.body = resp_json

    def on_post(self,req, resp):
        config = ConfigParser()
        config.read('config.ini')
        url = req.get_param("original_url", required=True)
        shortened_url = "b."+str(randint(1000,9999))+url[0:5]
        conn = redis.Redis(config.get('redis', 'host'),db=3)
        conn.set(shortened_url,url)
        resp.body=shortened_url



api = falcon.API()
api.add_route('/shorten_url', Url())
api.add_route('/get_url',Url())

if __name__ == '__main__':
   run_simple('localhost', 1234, api, use_reloader=True, passthrough_errors=True)
