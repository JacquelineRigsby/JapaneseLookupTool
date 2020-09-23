
import csv
import sqlite3

# Initialize connection to db
import sys


def connectDB():
    con = sqlite3.connect('jDictDB.db')
    return con

# Create new table, name supplied via arg
def newTable(con, tablename):
    cur = con.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS ''' + tablename + '''
             ([Romaji] text, [Katakana] text, [Hiragana] text, [Furigana] text, [Entries] text, [Characters] text)'''
    cur.execute(sql)
    con.commit()

# Return list of all tables in db
def getTables(con):
    cur = con.cursor()
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    cur.execute(sql)
    tableList = []
    for name in cur:
        tableList.append(name)
    return tableList

# Return list of column Romaji from table chosen via arg
def listTable(con, table):
    cur = con.cursor()
    if table is None:
        return None
    sql = 'SELECT Romaji FROM ' + table
    try:
        cur.execute(sql)
    except sqlite3.OperationalError as e:
        print(sys.exc_info()[0])
    list = cur.fetchall()
    con.commit()
    return list

# Insert a record into table chosen via arg
def insertWord(con, table, r, k, h, f, e, c):
    sql = '''INSERT INTO ''' + table + '''(Romaji, Katakana, Hiragana, Furigana, Entries, Characters)
                  VALUES(?, ?, ?, ?, ?, ?)'''
    cur = con.cursor()
    cur.execute(sql, (r, k, h, f, e, c))
    con.commit()

# Select all records from a table arg based on romaji arg, return as list
def selectWord(con, word, table):
    cur = con.cursor()
    if table is None:
        return None
    sql = 'SELECT Romaji, Katakana, Hiragana, Furigana, Entries, Characters FROM ' + table + ' WHERE Romaji=?'
    cur.execute(sql, (word,))
    result = cur.fetchall()
    words = []
    for i in result:
        for j in i:
            words.append(j)
    con.commit()
    return words

# Delete record from table arg based on romaji arg
def deleteWord(con, word, table):
    sql = 'DELETE FROM ' + table + ' WHERE Romaji=?'
    cur = con.cursor()
    cur.execute(sql, (word,))
    con.commit()

# Drop table arg
def dropTable(con, table):
    sql = 'DROP TABLE IF EXISTS ' + table
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def exportCSV(con, table):
    try:
        sql = 'SELECT * FROM ' + table
        cur = con.cursor()
        cur.execute(sql)
        results = cur.fetchall()

        headers = [i[0] for i in cur.description]

        csvFile = csv.writer(open(table.strip("''") + '.csv', 'w', encoding="utf-8", newline=''),
                             delimiter=',', lineterminator='\r\n',
                             escapechar='\\')
        csvFile.writerow(headers)
        csvFile.writerows(results)
    except sqlite3.DatabaseError as e:
        print(sys.exc_info()[0])





