from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
app.json.sort_keys = False



# method   search/topic
@app.route('/search/<string:topic>', methods=['GET'])
def search_book(topic):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    if topic.lower()=="distributed systems".lower():
        cursor.execute("SELECT * FROM books WHERE id IN (1, 2)")
        books = cursor.fetchall()
    elif topic.lower()=="undergraduate school".lower():
        cursor.execute("SELECT * FROM books WHERE id IN (3, 4)")
        books = cursor.fetchall()
    else:
        books = None
    conn.close()

    if books is not None:
        response_data = [
                    {
                        "id": book[0],
                        "title": book[1],
                        "author": book[2],
                        "quantity": book[3],
                        "price": book[4]
                    }
                    for book in books
                ]
    else:
        response_data = {
            'status':'topic not found'
        }
        
    
    return jsonify(response_data)


# method    info
@app.route('/info/<int:book_id>', methods=['GET'])
def get_book_info(book_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()

    if book is not None:
        response_data =  {
                    "id" : book[0],
                    "title": book[1],
                    "author": book[2],
                    "quantity": book[3],
                    "price": book[4]
                }
    else:
        response_data = None
    
    return jsonify(response_data)



# connection between catalog and order server
@app.route('/catalog/<int:book_id>', methods=['PUT'])
def get_book_info_and_update(book_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    #chek if book found
    if book is None:
        response_data =  {
                'status':'Book not found'
                }
        return jsonify(response_data)


    #chek if quantity is empty
    if book[3]<=0:
        response_data =  {
                'status':'sorry,The quantity is empty'
                }
        return jsonify(response_data)

    
    #decrement quantity one and save
    new_value=book[3]-1
    cursor.execute("UPDATE books SET quantity = ? WHERE id = ?", (new_value , book_id))
    conn.commit()
    response_data =  {
                "status":"purchase successfully"
                }
    
    return jsonify(response_data)

    

if __name__ == '__main__':
    app.run(debug=True,host='172.17.0.2',port=5100)