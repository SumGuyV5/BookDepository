"""***************************************************************
**  Program Name:   BookDepository				**
**  Version Number: V0.9                                        **
**  Copyright (C):  February 16, 2017 Richard W. Allen          **
**  Date Started:   October 1, 2016                             **
**  Date Ended:     February 16, 2017                           **
**  Author:         Richardn W. Allen                           **
**  Webpage:        http://www.richardallenonline.com/          **
**  IDE:            IDLE 2.7.11                                 **
**  Compiler:       Python 2.7.11                               **
**  Langage:        Python 2.7.11				**
**  License:	    GNU GENERAL PUBLIC LICENSE Version 2	**
**		    see license.txt for for details	        **
***************************************************************"""
#!/usr/bin/python
import sqlite3
import inspect
from datetime import datetime

class ItemsDataset:
    _id = 0
    _number = 0
    _price = 0.00
    _datetime = datetime.now()
    
    def __init__(self, id = 0, number = 0, price = 0.0, timedate = datetime.now()):
        self._id = id
        self._number = number
        self._price = price
        if isinstance(timedate, basestring):
            self._datetime = datetime.strptime(timedate, "%Y-%m-%d %H:%M:%S.%f")
        else:
            self._datetime = timedate
    
    def Insert(self):        
        return (ITEMS.InsertText(), self.__ReturnAll() )
    
    def __ReturnAll(self):
        return ( self._number, self._price, self._datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
class LowestDataset:
    _number = 0
    _price = 0.0;
    _datetime = datetime.now()
    
    def __init__(self, number = 0, price = 0.0, timedate = datetime.now()):
        self._number = number
        self._price = price
        if isinstance(timedate, basestring):
            self._datetime = datetime.strptime(timedate, "%Y-%m-%d %H:%M:%S.%f")
        else:
            self._datetime = timedate
    
    def Update(self, price):
        if (self._price > price):
            self._price = price
            self._datetime = datetime.now();     
    
    def Insert(self):
        return (LOWEST.InsertText(), self.__ReturnAll())
    
    def __ReturnAll(self):
        return (self._number, self._price, self._datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
class UnavailableDataset:
    _number = 0
    _datetime = datetime.now()
    
    def __init__(self, number = 0, timedate = datetime.now()):
        self._number = number
        if isinstance(timedate, basestring):
            self._datetime = datetime.strptime(timedate, "%Y-%m-%d %H:%M:%S.%f")
        else:
            self._datetime = timedate
    
    def Update(self):
        self._datetime = datetime.now();     
    
    def Insert(self):
        return (UNAVAILABLE.InsertText(), self.__ReturnAll())
    
    def __ReturnAll(self):
        return (self._number, self._datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))

class ITEMS:
    TABLE_NAME = 'items'
    COLUMN_ID = 'ID'
    COLUMN_NUMBER = 'NUMBER'
    COLUMN_PRICE = 'PRICE'
    COLUMN_DATETIME = 'DATETIME'
    
    ALL_COLUMNS = [COLUMN_ID, COLUMN_NUMBER, COLUMN_PRICE, COLUMN_DATETIME]
    
    TABLE_CREATE = ("CREATE TABLE " + TABLE_NAME +
        "(" + COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        COLUMN_NUMBER + " INT NOT NULL, " +
        COLUMN_PRICE + " REAL NOT NULL, " +
        COLUMN_DATETIME + " REAL NOT NULL) ")
    
    @staticmethod
    def InsertText():
        return "INSERT INTO " + ITEMS.TABLE_NAME + ITEMS.ColumnText() + " VALUES(?, ?, ?)"
    
    @staticmethod
    def ColumnText():
        columntxt = "("
        for idx,column in enumerate(ITEMS.ALL_COLUMNS):
            if idx > 0:
                columntxt += column
                if idx < (len(ITEMS.ALL_COLUMNS) - 1):
                    columntxt += ", "
        columntxt += ") "
        return columntxt
        
class LOWEST:
    TABLE_NAME = 'lowest'
    COLUMN_NUMBER = 'NUMBER'
    COLUMN_PRICE = 'PRICE'
    COLUMN_DATETIME = 'DATETIME'
    
    ALL_COLUMNS = [COLUMN_NUMBER, COLUMN_PRICE, COLUMN_DATETIME]
    
    TABLE_CREATE = ("CREATE TABLE " + TABLE_NAME +
        "(" + COLUMN_NUMBER + " INT NOT NULL, " +
        COLUMN_PRICE + " REAL NOT NULL, " +
        COLUMN_DATETIME + " REAL NOT NULL) ")
    
    @staticmethod
    def InsertText():
        return "INSERT INTO " + LOWEST.TABLE_NAME + LOWEST.ColumnText() + " VALUES(?, ?, ?)"
    
    @staticmethod
    def UpdateText():
        return ("UPDATE " + LOWEST.TABLE_NAME + " set " + LOWEST.COLUMN_PRICE + "={0}, " + LOWEST.COLUMN_DATETIME + 
        "='{1}' where " + LOWEST.COLUMN_NUMBER + "={2}")
    
    @staticmethod
    def ColumnText():
        columntxt = "("
        for idx,column in enumerate(LOWEST.ALL_COLUMNS):
            columntxt += column
            if idx < (len(LOWEST.ALL_COLUMNS) - 1):
                columntxt += ", "
        columntxt += ") "
        return columntxt

class UNAVAILABLE:
    TABLE_NAME = 'Unavailable'
    COLUMN_NUMBER = 'NUMBER'
    COLUMN_DATETIME = 'DATETIME'
    
    ALL_COLUMNS = [COLUMN_NUMBER, COLUMN_DATETIME]
    
    TABLE_CREATE = ("CREATE TABLE " + TABLE_NAME +
        "(" + COLUMN_NUMBER + " INT NOT NULL, " +
        COLUMN_DATETIME + " REAL NOT NULL) ")
    
    @staticmethod
    def InsertText():
        return "INSERT INTO " + UNAVAILABLE.TABLE_NAME + UNAVAILABLE.ColumnText() + " VALUES(?, ?)"
    
    @staticmethod
    def UpdateText():
        return ("UPDATE " + UNAVAILABLE.TABLE_NAME + " set " + UNAVAILABLE.COLUMN_DATETIME + 
        "='{0}' where " + UNAVAILABLE.COLUMN_NUMBER + "={1}")
        
    @staticmethod
    def Delete():
        return ("DELETE FROM " + UNAVAILABLE.TABLE_NAME + " WHERE " + UNAVAILABLE.COLUMN_NUMBER + "={0}")
    
    @staticmethod
    def ColumnText():
        columntxt = "("
        for idx,column in enumerate(UNAVAILABLE.ALL_COLUMNS):
            columntxt += column
            if idx < (len(UNAVAILABLE.ALL_COLUMNS) - 1):
                columntxt += ", "
        columntxt += ") "
        return columntxt

class SQLDatabase:
    __allTablesCreate = [ITEMS.TABLE_CREATE, LOWEST.TABLE_CREATE, UNAVAILABLE.TABLE_CREATE]
    __databaseName = 'bookdepository.db'
    __conn = sqlite3.connect(__databaseName)
    def __init__(self):
        for table in self.__allTablesCreate:
            try:
                self.__conn.execute(table)
            except sqlite3.OperationalError:
                print "{0} already exists.".format(table)
    
    def __del__(self):
        self.__conn.close()
        
    def create(self, dataset):
        cur = self.__conn.cursor()
        
        txt, data = dataset.Insert()
              
        cur.execute(txt, data)
        
        rtn = cur.lastrowid
        
        self.__conn.commit()
        
        return rtn
        
    def Get(self, tableName, id = 0):
        rtn = []
        sql = "SELECT * from " + tableName
        
        if id > 0:
            if tableName == ITEMS.TABLE_NAME:
                    sql += " where " + ITEMS.COLUMN_ID + "=" + id
            elif tableName == UNAVAILABLE.TABLE_NAME:
                sql += " where " + UNAVAILABLE.COLUMN_NUMBER + "=" + str(id)
        cursor = self.__conn.execute(sql)
        if tableName == ITEMS.TABLE_NAME:
            for row in cursor:
                rtn.append(ItemsDataset(row[0], row[1], row[2], row[3], row[4]))
        elif tableName == LOWEST.TABLE_NAME:
            for row in cursor:
                rtn.append(LowestDataset(row[0], row[1], row[2]))
        elif tableName == UNAVAILABLE.TABLE_NAME:
            for row in cursor:
                rtn.append(UnavailableDataset(row[0], row[1]))
            
        return rtn
    
    def Del(self, tableName, number):
        txt = ""            
        if tableName == UNAVAILABLE.TABLE_NAME:
            txt = UNAVAILABLE.Delete().format(number)
        print txt
        cur = self.__conn.cursor()
        cur.execute(txt)
        self.__conn.cursor()
    
    def Update(self, dataset):
        txt = LOWEST.UpdateText().format(dataset._price, str(dataset._datetime), dataset._number)
        print txt
        cur = self.__conn.cursor()
        cur.execute(txt)
        self.__conn.commit()

class Database:
    __sql = SQLDatabase()
    __items = []
    __lowest = []
    __unavailable = []
    
    def __init__(self):
        #self.__items = self.__sql.Get(ITEMS.TABLES_NAME)
        self.__LowestLoad()
        self.__UnavailableLoad()
        
    def __del__(self):
        del self.__sql       
        
    def GetItems(self):
        return self.__items
    
    def GetLowest(self):
        return self.__lowest
    
    def GetUnavailable(self):
        return self.__unavailable
    
    def AddUnavailable(self, dataset):
        rtn = True
        if self.__UpdateUnavailableCheck(dataset) == False:
            self.__sql.create(dataset)
            self.__UnavailableLoad()
        return rtn
    
    def AddItem(self, dataset):
        rtn = False
        id = self.__sql.create(dataset)
        found, lower = self.__UpdateLowestCheck(dataset)
        rtn = lower    
        if found == False:
            self.__sql.create(LowestDataset(dataset._number, dataset._price, datetime.now()))
            rtn = True
        if rtn == True:
            self.__LowestLoad()
        return rtn
    
    def RemoveUnavailable(self, dataset):
        rtn = False
        tmp = self.__sql.Get(UNAVAILABLE.TABLE_NAME, dataset._number)
        if len(tmp) > 0:
            self.__sql.Del(UNAVAILABLE.TABLE_NAME, dataset._number)
            self.__UnavailableLoad()
            rtn = True
        return rtn
        
    def __UpdateUnavailableCheck(self, dataset):
        for idx,low in enumerate(self.__unavailable):
            if low._number == dataset._number:
                return True
        return False
    
    def __UpdateLowestCheck(self, dataset):
        found = False
        for idx,low in enumerate(self.__lowest):
            if low._number == dataset._number:
                found = True
                if low._price > dataset._price:
                    print low._price
                    print dataset._price
                    self.__lowest[idx]._price = dataset._price
                    self.__lowest[idx]._datetime = datetime.now()
                    self.__sql.Update(self.__lowest[idx])
                    return (found, True)
        return (found, False)
    
    def __UnavailableLoad(self):
        self.__unavailable = self.__sql.Get(UNAVAILABLE.TABLE_NAME)                
                
    def __LowestLoad(self):
        self.__lowest = self.__sql.Get(LOWEST.TABLE_NAME)
        
                
                
             

def main():
    pass
    #tmp = SQLDatabase()
    
    #item = ItemsDataset()
    #lowest = LowestDataset()
    
    #dataset = tmp.Get(LOWEST.TABLE_NAME)
    
    #print dataset[0]._number
    #print dataset[0]._price
    #print dataset[0]._datetime
        
    #dataset[0]._price = 100.50
    #dataset[0]._datetime = datetime.now()
    
    #tmp.Update(dataset[0])
    
    #dataset = tmp.Get(LOWEST.TABLE_NAME)
    
    #print dataset[0]._price
    #print dataset[0]._datetime
    
    
    
    #tmp.create(lowest)

#if __name__ == "__main__":
   # main()
