import sqlite3

conn = sqlite3.connect("nba.db")

c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE game
#              (date text, winner text, loser text)''')

f = open("./info/1946-47.txt")
tmp = f.readlines()
f.close()

for i in tmp:
    if i.split()[0][0] != "=":
        date = i.split()[0]
        w = i.split()[3]
        l = i.split()[6]
        c.execute("INSERT INTO game VALUES ('{}', '{}', '{}')".format(date, w, l))

# # Insert a row of data
# c.execute("INSERT INTO nba VALUES ({}, {}, {})".format(date, w, l))

# Save (commit) the changes
conn.commit()

c.execute("SELECT * FROM game")
for i in c:
    print(i)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

