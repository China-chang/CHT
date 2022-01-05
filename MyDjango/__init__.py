import pymysql
pymysql.version_info = (1, 4, 0, 'final', 0)
#将pymysql起个别名为MySQLdb
pymysql.install_as_MySQLdb()