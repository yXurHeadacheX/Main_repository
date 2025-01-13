import sqlite3

connection = sqlite3.connect('cryptocurrency.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS cryptocurrency(
    НАИМЕНОВАНИЕ TEXT,
    СИМВОЛ TEXT,
    РЫЧОЧНАЯ_КАПИТАЛИЗАЦИЯ TEXT,
    ЦЕНА TEXT
)
               """)

connection.commit()

f = open('for_classes_basa.txt')

#cursor.execute("SELECT * FROM value")
#result = cursor.fetchall()
N = f.readline()
x = []
for i in f:
    x.append(i.split())
for i in range(len(x)):
    cursor.execute("INSERT INTO cryptocurrency VALUES (?,?,?,?)", (x[i][0],x[i][1],'₽'+x[i][2],'₽'+x[i][3]))
connection.commit()
