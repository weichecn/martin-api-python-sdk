#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenbingyu@buding.cn'

from datetime import datetime
from hashlib import md5

from requests import Request, Session


class Client(object):
    def __init__(self, app_key, app_secret, host=None):
        self.app_key = app_key
        self.app_secret = app_secret
        if host:
            self.host = host
        else:
            self.host = 'http://api.buding.cn'

    def get(self, api):
        session = Session()
        req = Request('get', self.host + api).prepare()
        headers = self.gen_headers('GET', api, 0)
        req.headers.update(headers)
        resp = session.send(req)
        return resp.json()

    def post(self, api, **kwargs):
        session = Session()
        req = Request('post', self.host + api, data=kwargs).prepare()
        headers = self.gen_headers('POST', api, req.headers['Content-Length'])
        req.headers.update(headers)
        resp = session.send(req)
        return resp.json()

    def gen_headers(self, method, api, content_length):
        headers = {}
        now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_list = [
            method,
            api,
            now,
            str(content_length),
            md5.new(self.app_secret).hexdigest()
        ]
        signature = md5.new('&'.join(signature_list)).hexdigest()

        headers['Host'] = self.host
        headers['Date'] = now
        headers['Authorization'] = '%s:%s' % (self.app_key, signature)
        return headers