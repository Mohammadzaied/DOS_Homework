from flask import Flask, jsonify
import requests

app = Flask(__name__)
app.json.sort_keys = False

catalog_url = 'http://172.17.0.2:5100'
order_url='http://172.17.0.4:5200'


# method  search 
@app.route('/search/<string:topic>', methods=['GET'])
def search_books(topic):
    catalog_response = requests.get(f"{catalog_url}/search/{topic}")
    return catalog_response.json()
    


# method    info
@app.route('/info/<int:book_id>', methods=['GET'])
def get_book_info(book_id):
    catalog_response = requests.get(f"{catalog_url}/info/{book_id}")
    return catalog_response.json()



# method   purchase
@app.route('/purchase/<int:book_id>', methods=['GET'])
def purchase_book(book_id):
    catalog_response = requests.put(f"{order_url}/purchase/{book_id}")
    return catalog_response.json()


if __name__ == '__main__':
    app.run(debug=True,host='172.17.0.3',port=5000)