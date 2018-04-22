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
hasher = hashlib.sha256()

# Window
#window = Tk()
#window.withdraw()
c = 0

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

# Loop on files in selected folder and sub-folders
for root, dirs, filenames in os.walk(root):
	for f in filenames:
		# Open file in binary mode
		log = open(os.path.join(root, f), 'rb')
		while True:
			data = log.read(BUF_SIZE);
			if not data:
				break
			# Get file hash
			hasher.update(data)
			# Insert new row for file
			file = [(f, format(hasher.hexdigest()), time.time())]
			print(file)
			c.executemany("INSERT INTO files VALUES(?,?,?)", file)

# End timer by retrieving current time
finish = time.time()
# Substract
timeElapsed = finish-start

print("\nResults :\n")
for row in c.execute("SELECT * FROM files"):
	print(row)

print("\nDone")
print("Time elapsed :", timeElapsed)


