# -*- coding: utf-8 -*-


import pyodbc

def insertWord2DbEV(nameCol1, nameCol2, English, Vietnamese):
	con = pyodbc.connect("Driver={SQL Server};server=NAMTRUNG205-NB\SQLEXPRESS;database=EVDictionary;")
	cur= con.cursor()


	sql = str("insert into dbo.EVDic({0},{1}) values (?, ?)").format(nameCol1, nameCol2)
	val = (English, Vietnamese)
	# print(sql)
	cur.execute(sql, val)
	cur.commit()
	# print("Da insert du lieu thanh cong!")

	cur.close()
	con.close()

# update row
def updateARow(primaryRecord, updateValue):
	con = pyodbc.connect("Driver={SQL Server};server=NAMTRUNG205-NB\SQLEXPRESS;database=EVDictionary;")
	cur= con.cursor()

	QueryCommand = "UPDATE dbo.EVDic SET Vietnamese=N'{0}' WHERE EVDic.English=?".format(updateValue)
	val = primaryRecord

	cur.execute(QueryCommand, val)
	cur.commit()

	cur.close()
	con.close()

# Check exit record
def checkExitsRecord(primaryRecord):
	con = pyodbc.connect("Driver={SQL Server};server=NAMTRUNG205-NB\SQLEXPRESS;database=EVDictionary;")
	cur= con.cursor()

	QueryCommand = "SELECT TOP 1 English,Vietnamese FROM EVDic WHERE English=?"
	val = primaryRecord

	cur.execute(QueryCommand, val)
	countRecord = len(list(cur))
	cur.commit()
	cur.close()
	con.close()

	if countRecord == 0:
		return False
	else:
		return True
