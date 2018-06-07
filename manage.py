#!venv/bin/python
# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
from flask import *
import warnings
warnings.filterwarnings("ignore")
import MySQLdb
import MySQLdb.cursors
from config import *
from app  import app


# 连接数据库
def connectdb():
    db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
    db.autocommit(True)
    cursor = db.cursor()
    return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
    db.close()
    cursor.close()

if __name__ == '__main__':
    app.run(SERVERHOST,SERVERPORT,debug=True)
