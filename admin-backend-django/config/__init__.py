import pymysql

# PyMySQL reemplaza a mysqlclient (difícil de instalar en Windows).
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()