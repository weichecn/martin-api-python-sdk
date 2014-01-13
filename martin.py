#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenbingyu@buding.cn'

from datetime import datetime
from hashlib import md5
from json import loads

from requests import Request, Session


class APIError(StandardError):
    def __init__(self, ret_error):
        self.responce = ret_error
        StandardError.__init__(self, ret_error['msg'])

    def __str__(self):
        return '***%s %s*** %s' % (
            self.responce['code'],
            self.responce['msg'],
            self.responce['request'])


class Client(object):
    def __init__(self, app_key, app_secret, api_host=None):
        self.app_key = app_key
        self.app_secret = app_secret
        if api_host:
            self.api_host = api_host
        else:
            self.api_host = 'http://api.buding.cn'

    def get(self, api):
        session = Session()
        req = Request('get', self.api_host + api).prepare()
        headers = self.gen_headers('GET', api, 0)
        req.headers.update(headers)
        responce = session.send(req)
        try:
            ret = loads(responce.content)
        except ValueError, e:
            return resp.content
        if 'msg' in ret and 'code' in ret:
            raise APIError(ret)

        return ret

    def post(self, api, **kwargs):
        session = Session()
        req = Request('post', self.api_host + api, data=kwargs).prepare()
        headers = self.gen_headers('POST', api, req.headers['Content-Length'])
        req.headers.update(headers)
        responce = session.send(req)
        try:
            ret = loads(responce.content)
        except ValueError, e:
            return resp.content
        if 'msg' in ret and 'code' in ret:
            raise APIError(ret)
        return ret

    def gen_headers(self, method, api, content_length):
        headers = {}
        now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_list = [
            method,
            api,
            now,
            str(content_length),
            md5(self.app_secret).hexdigest()
        ]
        signature = md5('&'.join(signature_list)).hexdigest()

        headers['Date'] = now
        headers['Authorization'] = '%s:%s' % (self.app_key, signature)
        return headers
