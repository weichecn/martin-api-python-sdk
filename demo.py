#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenbingyu'

from time import sleep

import martin


app_key = 'YOUR_APP_KEY'
app_secret = 'YOUR_APP_SECRET'


def query_violations_v1(license_plate_num, engine_num, body_num, city):
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


def query_violations_v2(license_plate_num, engine_num, body_num, city):
    ret = client.post(
        '/v2/jobs',
        license_plate_num=license_plate_num,
        engine_num=engine_num,
        body_num=body_num,
        city_pinyin=city)
    job_id = ret['id']
    while True:
        try:
            ret = client.get('/v2/job/%s' % job_id)
        except martin.APIError, e:
            if e.responce['code'] == 1005:
                # get captcha image
                captcha = e.responce['captcha']
                captcha_data = client.get('/v2/captcha/%s/img' % captcha['id'])
                f = open('captcha.jpeg', 'wb')
                f.write(f)
                f.close()
                captcha_text = raw_input('captcha: ')

                # verify captcha
                client.post(
                    '/v2/captchas/verify',
                    id=captcha['id'],
                    captcha=captcha_text)

        if ret['status'] in ['finished', 'failed']:
            print ret
            break
        else:
            sleep(ret['sleep'])


if __name__ == '__main__':
    try:
        query_violations_v1(u'京XXXXXX', 'XXXXXX', 'XXXXXX', 'beijing')
    except martin.APIError, e:
        print e
