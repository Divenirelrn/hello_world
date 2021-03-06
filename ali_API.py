#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import base64
import hmac
import hashlib
import json
from flask import Flask
import urllib

def get_current_date():
    date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
    return date
def to_md5_base64(strBody):
    hash = hashlib.md5()
    print(body)
    hash.update(body.encode('utf-8'))
    return hash.hexdigest()
    #return hash.digest().encode('base64').strip()
def to_sha1_base64(stringToSign, secret):
    print('secret:',secret)
    print('stringToSign:',stringToSign)
    #print(type(hashlib.sha1))
    hmacsha1 = hmac.new(secret.encode(encoding="utf-8"), stringToSign.encode(encoding="utf-8"), hashlib.sha1)
    return base64.b64encode(hmacsha1.digest())
ak_id = 'LTAI4FgTH1dmhPH7UkTVvQi6'
ak_secret = 'LTAI4FgTH1dmhPH7UkTVvQi6'
options = {
    'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/image/tag',
    'method': 'POST',
    'body': json.dumps({"name": "hello"}, separators=(',', ':')),
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'date':  get_current_date(),
        'authorization': ''
    }
}
# options = {
#     'url': '<请求的url>',
#     'method': 'GET',
#     'headers': {
#         'accept': 'application/json',
#         'content-type': 'application/json',
#         'date': get_current_date(),  # 'Sat, 07 May 2016 08:19:52 GMT',  # get_current_date(),
#         'authorization': ''
#     }
# }
body = ''
if 'body' in options:
    body = options['body']
print(body)
bodymd5 = ''
if not body == '':
    bodymd5 = to_md5_base64(body)
print(bodymd5)
urlPath = urllib.parse.urlparse(options['url'])
if urlPath.query != '':
    urlPath = urlPath.path + "?" + urlPath.query
else:
    urlPath = urlPath.path
stringToSign = options['method'] + '\n' + options['headers']['accept'] + '\n' + bodymd5 + '\n' + options['headers']['content-type'] + '\n' + options['headers']['date'] + '\n' + urlPath
signature = to_sha1_base64(stringToSign, ak_secret)
print(stringToSign)
print(type(ak_id))
print(signature)
authHeader = 'Dataplus ' + ak_id + ':' + base64.b64decode(signature)
options['headers']['authorization'] = authHeader
print(authHeader)
request = None
method = options['method']
url = options['url']
print(method)
print(url)
if 'GET' == method or 'DELETE' == method:
    request = urllib.Request(url)
elif 'POST' == method or 'PUT' == method:
    request = urllib.Request(url, body)
request.get_method = lambda: method
for key, value in options['headers'].items():
    request.add_header(key, value)
try:
    conn = urllib.urlopen(request)
    response = conn.read()
    print(response)
except urllib.HTTPError as e:
    print(e.read())
    raise SystemExit(e)