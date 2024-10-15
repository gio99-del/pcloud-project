from requests import get, post, head
import logging
'''
import http.client
http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''
#base_url = 'https://oceanic-throne-435807-j7.oa.r.appspot.com'
base_url = 'http://localhost:8080/'

t = get(f'{base_url}/client')
c = int(t.text)
print(c)

with open('crime.csv') as f:
    s = f.readline()
    dict_tag = []
    for x in s.split(','):
        dict_tag.append(x.strip('"').strip('"\n'))

    for line in f.readlines()[c:]:
        crime = {}
        i = 0
        for y in line.split('","'):
            crime.update({dict_tag[i]: y.strip('"').strip('"\n')})
            i += 1
        print(crime)
        r = post(f'{base_url}/data', data=crime)
