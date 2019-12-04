from decouple import config
import requests



markers1_prefix = 'color:blue|size:tiny'
markers1 = '|-25, -25|25, -25|25, 25|-25, 25'
markers2_prefix = 'color:red|size:tiny'
markers2 = '|45, 45|-45, -45|45, -45|-45, 45'


# status map
url1 = 'https://maps.googleapis.com/maps/api/staticmap'
params1 = {'center': '0, 0',
           'zoom': '2',
           'size': '1024x780',
           'markers': [markers1_prefix + markers1, markers2_prefix + markers2],
           'key': config('API_KEY')
          }

try:
    res = requests.get(url1, params=params1)

except requests.exceptions.ConnectionError:
    print('unable to get map')
    exit()

# save as file
pic_file = 'googlemap.png'
with open(pic_file, 'wb') as pic:
    pic.write(res.content)

# interactive map in a browser
url2 = 'https://www.google.com/maps/dir/?api=1'
params2 = {'center': '0, 0',
           'zoom': '2',
           'waypoints': markers1 + markers2,
          }

try:
    res = requests.get(url2, params=params2)

except requests.exceptions.ConnectionError:
    print('unable to get map')
    exit()

# use url to paste in browser
print(res.url)




