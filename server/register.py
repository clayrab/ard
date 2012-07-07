import hashlib
import sys
import MySQLdb

hashFunction = hashlib.sha256()
if(len(sys.argv) < 3):
    print "usage: python register.py username password"
    exit()
else:
    conn = MySQLdb.connect (host = "localhost",user = "clayrab_ard",passwd = "96c91f98",db = "clayrab_ard")
    cursor = conn.cursor() 
    hashFunc = hashlib.sha256()
    hashFunc.update(sys.argv[2])
    print sys.argv[1]
    print sys.argv[2]
    print "inserting"
    print sys.argv[1]
    print hashFunc.hexdigest()
    print hashFunc.digest_size
    execu = "INSERT INTO users (username, passhash) VALUES ('" + sys.argv[1] + "', '" + hashFunc.hexdigest()  + "')"
#    execu = "INSERT INTO users (username, passhash) VALUES ('%s', '%s')"
    print execu
    cursor.execute(execu)
    cursor.close()
    conn.commit()
    conn.close()
print 'done'




