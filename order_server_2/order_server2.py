from flask import Flask
import requests

app = Flask(__name__)


class RoundRobinSelector:
    def __init__(self, servers):
        self.servers = servers
        self.counter = 0

    def get_next_server(self):
        index = self.counter % len(self.servers)
        self.counter += 1
        return self.servers[index]

catalog_servers = ['http://172.17.0.4:5101','http://172.17.0.3:5100']
catalog_selector = RoundRobinSelector(catalog_servers)

def get_catalog_server():
    #  round-robin selection an catalog server
     return catalog_selector.get_next_server()

@app.route('/purchase/<int:book_id>', methods=['PUT'])
def purchase_book(book_id):
    catalog_server_url = get_catalog_server()    
    catalog_response = requests.put(f"{catalog_server_url}/update/{book_id}")
    return catalog_response.json()

@app.route('/add/<int:book_id>', methods=['PUT'])
def add_book(book_id):
    catalog_server_url = get_catalog_server() 
    catalog_response = requests.put(f"{catalog_server_url}/update2/{book_id}")
    return catalog_response.json()

if __name__ == '__main__':
    app.run(debug=True,host='172.17.0.6',port=5201)

