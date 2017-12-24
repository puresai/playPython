import pymysql
import types

class MySQL:
    __db = None

    # 在这里配置自己的SQL服务器
    __config = {
        'host':"127.0.0.1",
        'port':3306,
        'username':"root",
        'password':"",
        'database':"sai",
        'charset' :"utf8"
    }

    def __init__(self):
        self.__connect()

    def __del__(self):
        if(self.__db is not None):
            self.__db.close()

    def __connect(self):
        if (self.__db == None):
            self.__db = pymysql.connect(
                host   =self.__config['host'],
                port   =self.__config['port'],
                user   =self.__config['username'],
                passwd =self.__config['password'],
                db     =self.__config['database'],
                charset=self.__config['charset']
            )
        return self.__db

    def getCursor(self, isDict = True):
        _par = ''
        if isDict == True:
            return self.__connect().cursor(cursor = pymysql.cursors.DictCursor)
        return self.__connect().cursor()

    def handleParam(params, con = 'and'):
        _sql = '1=1';
        if(isinstance(params, int)):
            _sql = 'id = %d'%params
        elif(isinstance(params, dict)):
            for (k, v) in params:
                if(isinstance(v, dict)):
                    v = handleParam(v, '')
                _sql += ' ' + con + ' ' + k + v
        return _sql

    def query(self, _sql):
        cursor = self.getCursor()
        try:
            cursor.execute(_sql)
            data = cursor.fetchall()
            # 提交到数据库执行
            self.__connect().commit()
        except:
            # 如果发生错误则回滚
            self.__connect().rollback()
            return False
        return data

    def insert(self, tableName, columns, data):
        cursor = self.getCursor()
        try:
            cursor.execute('insert into `%s` (%s) values (%s)'%(tableName, columns, data))
            self.__connect().commit()
        except:
            self.__connect().rollback()
            return False
        return int(cursor.lastrowid)

    def insertBatch(self, tableName, columns, data):
        cursor = self.getCursor()
        try:
            cursor.execute('insert into `%s` (%s) values (%s)'%(tableName, columns, data))
            self.__connect().commit()
        except:
            self.__connect().rollback()
            return False
        return int(cursor.lastrowid)

    def update(self, tableName, data, where):
        cursor = self.getCursor()
        _where = self.handleParam(where)
        _data = self.handleParam(data)
        try:
            cursor.execute('update `%s` set %s  where %s'%(tableName, _data, _where))
            self.__connect().commit()
        except:
            self.__connect().rollback()
            return False
        return cursor.rowcount

    def delete(self, tableName, where):
        cursor = self.getCursor()
        _where = self.handleParam(where)
        try:
            cursor.execute('delete from `%s` where %s'%(tableName, _where))
            self.__connect().commit()
        except:
            self.__connect().rollback()
            return False
        return cursor.rowcount

    def find(self, tableName, where, fields = '*'):
        cursor = self.getCursor()
        _where = self.handleParam(where)
        cursor.execute('select  %s from `%s` where %s'%(fields, tableName, _where))
        return cursor.fetchone()

    def findAll(self, tableName, where, fields = '*'):
        cursor = self.getCursor()
        _where = self.handleParam(where)
        cursor.execute('select  %s from `%s` where %s'%(fields, tableName, _where))
        return cursor.fetchall()