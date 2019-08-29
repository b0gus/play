# http://www.pythonchallenge.com/pc/return/disproportional.html

import xmlrpc.client

url = "http://www.pythonchallenge.com/pc/phonebook.php"

conn = xmlrpc.client.ServerProxy(url)
print(conn.system.listMethods())
print(conn.system.methodHelp("phone"))
print(conn.system.methodSignature("phone"))
print(conn.phone("Bert")) # from previous quiz

# http://www.pythonchallenge.com/pc/return/italy.html