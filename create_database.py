import sqlite3

# Connect to an SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor obxxject
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        quantity INT,
        price REAL
    )
''')

# Insert data into the table
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('How to get a good grade in DOS in 40 minutes a day', 'john',100,70))
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('RPCs for Noobs', 'hary',200,30))
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('Xen and the Art of Surviving Undergraduate School', 'mayas',9,15))
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('Cooking for the Impatient Undergrad', 'john',17,90))

cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('How to finish Project 3 on time', 'john',70,114))
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('Why theory classes are so hard', 'hary',30,130))
cursor.execute('INSERT INTO books (title, author,quantity,price) VALUES (?, ?, ? ,?)', ('Spring in the Pioneer Valley', 'mayas',20,55))
conn.commit()

# Query data from the table
cursor.execute('SELECT * FROM books')
books = cursor.fetchall()

# Print the results
for book in books:
    print(book)

# Close the database connection
conn.close()
