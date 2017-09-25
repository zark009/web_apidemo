import re
import json,requests 

def re_header(header,zoken):
    headers2 = []
    headers_disc = {}
    headers =''
    headers = re.split(':|\r|\n|\r\n', header)
    while '' in headers:
        headers.remove('')
    for i in headers:
        i = i.lstrip()
        headers2.append(i)

    for i in range(0, len(headers2), 2):
        headers_disc[headers2[i]] = headers2[i + 1]
        if(headers2[i]=='zoken'):
            headers_disc[headers2[i]]=zoken
    headers = headers_disc
    return headers


def user_token():
    url = "https://api.xxxxxxx.com/xxxxxxx/passport/login/passwordLoginByUserNew"
    data= {}
    headers = {'content-type': 'application/json','User-Agent': 'okhttp/3.6.0'}
    req = requests.post(url,data=json.dumps(data), headers=headers)
    print(req.json()['data']['token'])
    return req.json()['data']['token']

def car_token():
    url = "https://api.xxxxxxx.com/xxxxxxx/passport/login/passwordLoginByFreight"
    data = {}
    headers = {'content-type': 'application/json', 'User-Agent': 'okhttp/3.6.0'}
    req = requests.post(url, data=json.dumps(data), headers=headers)
    print(req.json()['data']['token'])
    return req.json()['data']['token']
