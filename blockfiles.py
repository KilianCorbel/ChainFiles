import hashlib
import sys
import os
import time
from tkinter import *
from tkinter import filedialog
import sqlite3

# Init
DATABASE = "blockfiles.db"
BUF_SIZE = 65536

# Hasher
sha256 = hashlib.sha256()
md5 = hashlib.md5()
sha1 = hashlib.sha1()

def hashAndInsert(root, hasher):
	print("Hashing function : ",hasher)
	# Loop on files in selected folder and sub-folders
	for root, dirs, filenames in os.walk(root):
		for f in filenames:
			# Open file in binary mode
			log = open(os.path.join(root, f), 'rb')
			while True:
				data = log.read();
				if not data:
					break
				# Get file hash
				hasher.update(data)
				# Insert new row for file
				hash = format(hasher.hexdigest())
				date = format(time.time())
				c.execute("INSERT INTO files VALUES(?,?,?)", (f, hash, date,))

# Window
#window = Tk()
#window.withdraw()

# Check if Database exists
if os.path.isfile(DATABASE):
	# Database Init
	conn = sqlite3.connect("blockfiles.db")
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
else:
	# Create database
	conn =sqlite3.connect("blockfiles.db")
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute('''CREATE TABLE files(file text, hash text, date text)''')

# Open filedialog
root = filedialog.askdirectory()
print("\nRoot directory : ", root)

# Start timer by retrieving current time
start = time.time()

# Hash and insert files
hashAndInsert(root, sha256)

# End timer by retrieving current time
finish = time.time()
# Substract
timeElapsed = finish-start

#print("\nResults :\n")
#c.execute("SELECT * FROM files")
#r = c.fetchall()
#for value in r:
 #   print(value[1])

print("\nDone")
print("Time elapsed :", timeElapsed)

# Commit changes to db and close it
conn.commit()
conn.close()



