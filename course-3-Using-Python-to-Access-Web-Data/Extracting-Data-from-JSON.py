'''Welcome Afonso Martingo from Using Python to Access Web Data

Extracting Data from JSON

In this assignment you will write a Python program somewhat similar to http://www.py4e.com/code3/json2.py. The program will prompt for a URL, read the JSON data from that URL using urllib and then parse and extract the comment counts from the JSON data, compute the sum of the numbers in the file and enter the sum below:

We provide two files for this assignment. One is a sample file where we give you the sum for your testing and the other is the actual data you need to process for the assignment.

Sample data: http://py4e-data.dr-chuck.net/comments_42.json (Sum=2553)
Actual data: http://py4e-data.dr-chuck.net/comments_2166376.json (Sum ends with 21)
You do not need to save these files to your folder since your program will read the data directly from the URL. Note: Each student will have a distinct data url for the assignment - so only use your own data url for analysis.
Data Format
The data consists of a number of names and comment counts in JSON as follows:

{
  comments: [
    {
      name: "Matthias"
      count: 97
    },
    {
      name: "Geomer"
      count: 97
    }
    ...
  ]
}
The closest sample code that shows how to parse JSON and extract a list is json2.py. You might also want to look at xml3.py to see how to prompt for a URL and retrieve data from a URL.

Sample Execution

$ python3 solution.py
Enter location: http://py4e-data.dr-chuck.net/comments_42.json
Retrieving http://py4e-data.dr-chuck.net/comments_42.json
Retrieved 2733 characters
Count: 50
Sum: 2...'''

import json 
import urllib.request
import ssl

# Ignore SSL certificate errors for HTTPS connections
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get URL from user input, with a default value if empty
url = input("Enter url: ")
if len(url) < 1:
    url = "http://py4e-data.dr-chuck.net/comments_42.json"

print('Retrieving', url)
# Open URL and read the data
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print("Retrieved", len(data), "characters")

# Parse JSON data
info = json.loads(data)

# Initialize counters
total = 0
count = 0

# Loop through each comment in the JSON data
for item in info["comments"]:
    count += 1
    total += item["count"]

# Print results
print('Count:', count)
print('Sum:', total)
