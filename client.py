from requests import get, post

base_url = 'https://oceanic-throne-435807-j7.oa.r.appspot.com'

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
        r = post(f'{base_url}/data', data=crime)
        print('ok')
