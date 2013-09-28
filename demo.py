#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenbingyu'

from time import sleep

import martin


app_key = 'YOUR_APP_KEY'
app_secret = 'YOUR_APP_SECRET'


def query_violations(license_plate_num, engine_num, body_num, city):
    client = martin.Client(app_key, app_secret)
    ret = client.post(
        '/v1/jobs',
        license_plate_num=license_plate_num,
        engine_num=engine_num,
        body_num=body_num,
        city_pinyin=city,
        callback_url='',
        no_wait='true'
    )

    while True:
        if ret['job_status'] in ['queued', 'started'] and ret['sleep'] > 0:
            sleep(ret['sleep'])
            ret = client.get('/v1/job/' + ret['job_id'])
        else:
            break
    print ret


if __name__ == '__main__':
    query_violations(u'京XXXXXX', 'XXXXXX', 'XXXXXX', 'beijing')