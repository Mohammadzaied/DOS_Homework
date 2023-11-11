from flask import Flask
import requests

app = Flask(__name__)

catalog_url = 'http://172.17.0.2:5100'

@app.route('/purchase/<int:book_id>', methods=['PUT'])
def purchase_book(book_id):

    catalog_response = requests.put(f"{catalog_url}/update/{book_id}")
    return catalog_response.json()

if __name__ == '__main__':
    app.run(debug=True,host='172.17.0.4',port=5200)