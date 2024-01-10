from flask import Flask, jsonify
import requests

app = Flask(__name__)

catalog_servers = ['http://172.17.0.3:5100', 'http://172.17.0.4:5101']
order_servers = ['http://172.17.0.5:5200', 'http://172.17.0.6:5201']

class RoundRobinSelector:
    def __init__(self, servers):
        self.servers = servers
        self.counter = 0

    def get_next_server(self):
        index = self.counter % len(self.servers)
        self.counter += 1
        return self.servers[index]

catalog_selector = RoundRobinSelector(catalog_servers)
order_selector = RoundRobinSelector(order_servers)

## list as cached memory
catalog_data_list = []

class BookInfo:
    def __init__(self, book_id, data):
        self.book_id = book_id
        self.data = data

def get_catalog_server():
    return catalog_selector.get_next_server()

def get_order_server():
    return order_selector.get_next_server()

def add_to_catalog_data_list(book_id, data):
    book_info = BookInfo(book_id, data)
    catalog_data_list.append(book_info)

def get_from_catalog_data_list(book_id):
    for book_info in catalog_data_list:
        if book_info.book_id == book_id:
            return book_info.data
    return None

# add books to cache when operation search
def search_books_from_list(topic):
     result = []
     if topic.lower() == 'distributed systems':
        # Return books with IDs 1, 2, 5 , 6 for the 'distributed systems' topic
        book_ids = [1 , 2 , 5 , 6]
        result.extend([book_info.data for book_info in catalog_data_list if book_info.book_id in book_ids])
        return result
    
     elif topic.lower() == 'undergraduate school':
        # Return books with IDs 3, 4, 7 for the 'undergraduate school' topic
        book_ids = [3, 4, 7]
        result.extend([book_info.data for book_info in catalog_data_list if book_info.book_id in book_ids])
        return result


# delete books from cache when operation update        
def delete_books_from_list(id):
    result = []
   
    if id in [1 , 2 , 5 , 6]:
        # Remove books with IDs 1, 2, 5, 6 for the 'distributed systems' topic
        book_ids_to_remove = [1 , 2 , 5 , 6]
        books_to_remove = [book_info for book_info in catalog_data_list if book_info.book_id in book_ids_to_remove]
        for book_info in books_to_remove:
            catalog_data_list.remove(book_info)
                

    elif id in [3, 4, 7]:
        # Remove books with IDs 3, 4, 7 for the 'undergraduate school' topic
        book_ids_to_remove = [3, 4, 7]
        books_to_remove = [book_info for book_info in catalog_data_list if book_info.book_id in book_ids_to_remove]
        for book_info in books_to_remove:
            catalog_data_list.remove(book_info) 




@app.route('/search/<string:topic>', methods=['GET'])
def search_books(topic):
    cached_data = search_books_from_list(topic)
    if cached_data:
        print("Cache hit!!!!!!!!!!!!!!!!!!!")
        return jsonify(cached_data)

    print("Cache miss. Making a server call...")
    catalog_server_url = get_catalog_server()
    catalog_response = requests.get(f"{catalog_server_url}/search/{topic}")
    json_data = catalog_response.json()

    for json in json_data:
        add_to_catalog_data_list(json['id'], json)

    return jsonify(json_data)



# info operation
@app.route('/info/<int:book_id>', methods=['GET'])
def get_book_info(book_id):
    cached_data = get_from_catalog_data_list(book_id)
    if cached_data:
        print("Cache hit!!!!!!!!!!!!!!!!!!!!!")
        return jsonify(cached_data)

    print("Cache miss. Making a server call...")
    catalog_server_url = get_catalog_server()
    catalog_response = requests.get(f"{catalog_server_url}/info/{book_id}")
    json_data = catalog_response.json()

    add_to_catalog_data_list(book_id, json_data)

    return jsonify(json_data)




# purchase operation
@app.route('/purchase/<int:book_id>', methods=['GET'])
def purchase_book(book_id):
    order_server_url = get_order_server()
    catalog_response = requests.put(f"{order_server_url}/purchase/{book_id}")
    
    # Delete items book from the list
    if catalog_response.status_code == 200:
        delete_books_from_list(book_id)
    return catalog_response.json()

# add operation
@app.route('/add/<int:book_id>', methods=['GET'])
def add_book(book_id):
    order_server_url = get_order_server()
    catalog_response = requests.put(f"{order_server_url}/add/{book_id}")
    
    # Delete items book from the list
    if catalog_response.status_code == 200:
        delete_books_from_list(book_id)
    return catalog_response.json()

if __name__ == '__main__':
    app.run(debug=True, host='172.17.0.2', port=5000)
