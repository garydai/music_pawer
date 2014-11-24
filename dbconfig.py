import MySQLdb as mdb
import socket


def connectDB():
    try:
        conn = mdb.connect(host='127.0.0.1',
                           user='root',
                           passwd='',
                           db='music',
                           charset='utf8')
        print "connet success"
        return conn
    except mdb.Error, e:
        print "Mysql Error, %s,%s"%(e.args[0],e.args[1])


if __name__ == '__main__':
	connectDB()
