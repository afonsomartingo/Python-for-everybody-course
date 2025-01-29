'''Welcome Afonso Martingo from Using Python to Access Web Data

Calling a JSON API

In this assignment you will write a Python program somewhat similar to http://www.py4e.com/code3/opengeo.py. The program will prompt for a location, contact a web service and retrieve JSON for the web service and parse that data, and retrieve the first plus_code from the JSON. An Open Location Code is a textual identifier that is another form of address based on the location of the address.
API End Points

To complete this assignment, you should use this API endpoint that has a static subset of the Open Street Map Data.

http://py4e-data.dr-chuck.net/opengeo?
This API also has no rate limit so you can test as often as you like. If you visit the URL with no parameters, you get "No address..." response.
To call the API, you need to provide the address that you are requesting as the q= parameter that is properly URL encoded using the urllib.parse.urlencode() function as shown in http://www.py4e.com/code3/opengeo.py


Test Data / Sample Execution

You can test to see if your program is working with a location of "South Federal University" which will have a plus_code of "6FV8QPRJ+VQ".

$ python solution.py
Enter location: South Federal University
Retrieving http://...
Retrieved 1290 characters
Plus code 6FV8QPRJ+VQ'''

import urllib.request, urllib.parse
import json, ssl

# Heavily rate limited proxy of https://www.geoapify.com/ api
serviceurl = 'http://py4e-data.dr-chuck.net/opengeo?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1: 
        break
    
    # Create parameters dictionary for the URL
    parms = dict()
    parms['q'] = address
    
    # Create the complete URL with encoded parameters
    url = serviceurl + urllib.parse.urlencode(parms)
    
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    
    try:
        # Parse JSON response
        js = json.loads(data)
    except:
        js = None
    
    if not js or 'features' not in js:
        print('==== Failure To Retrieve ====')
        print(data)
        continue
    
    # Extract and print the plus_code from the first result
    if len(js['features']) > 0:
        plus_code = js['features'][0]['properties']['plus_code']
        print('Plus code:', plus_code)
