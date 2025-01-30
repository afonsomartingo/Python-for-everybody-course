'''Counting Organizations
This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

CREATE TABLE Counts (org TEXT, count INTEGER)
When you have run the program on mbox.txt upload the resulting database file above for grading.
If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.

You can use this code as a starting point for your application: http://www.py4e.com/code3/emaildb.py.

The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.

Because the sample code is using an UPDATE statement and committing the results to the database as each record is read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely writing all the data to disk every time it is called.

The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program, there is a balance between the number of operations you execute between commits and the importance of not losing the results of operations that have not yet been committed.'''


import sqlite3

# Connect to database
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Drop existing table if any
cur.execute('DROP TABLE IF EXISTS Counts')

# Create the table
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Get filename from user input
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'

try:
    fhand = open(fname)
except:
    print('File cannot be opened:', fname)
    exit()

for line in fhand:
    if not line.startswith('From: '): 
        continue
    pieces = line.split()
    email = pieces[1]
    # Get organization (domain) from email address
    org = email.split('@')[1]
    
    # Look up the org in the database
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    
    if row is None:
        # If not found, insert new org with count 1
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else:
        # If found, update count
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

# Commit all changes at once (outside the loop for better performance)
conn.commit()

# Print the counts
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()