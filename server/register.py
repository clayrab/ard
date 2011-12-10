import hashlib
import sys
import MySQLdb

hashFunction = hashlib.sha256()
if(len(sys.argv) < 3):
    print "usage: python register.py username password"
    exit()
else:
    conn = MySQLdb.connect (host = "localhost",user = "clay",passwd = "maskmask",db = "ard")
    cursor = conn.cursor()
    hashFunc = hashlib.sha256()
    hashFunc.update(sys.argv[2])
    cursor.execute ("""
       INSERT INTO users (username, passhash)
       VALUES ('""" + sys.argv[1] + """', '""" + hashFunc.digest()  + """')
     """)
    cursor.close()
    conn.close()
print 'done'




