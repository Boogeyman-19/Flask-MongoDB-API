from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['tables']

# Insert three documents into the collection
documents = [
    {'name': 'John Doe', 'age': 30, 'city': 'New York'},
    {'name': 'Jane Smith', 'age': 25, 'city': 'Los Angeles'},
    {'name': 'Alice Johnson', 'age': 35, 'city': 'Chicago'}
]
result = collection.insert_many(documents)
print(f'Documents inserted with ids: {result.inserted_ids}')

@app.route('/')
def home():
    msg = "Avilable end points are :"
    eps =  "1. /create 2. /read  3. /read/{id} 4. /update/{id}  5. /delete/{id} "
    return f"{msg} {print(end="")} {eps}"
    

@app.route('/create', methods=['POST'])
def create_document():
    document = request.json
    result = collection.insert_one(document)
    return jsonify({'message': 'Document inserted', 'id': str(result.inserted_id)})

@app.route('/read', methods=['GET'])
def read_documents():
    documents = list(collection.find())
    for doc in documents:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return jsonify(documents)

@app.route('/read/<id>', methods=['GET'])
def read_document(id):
    document = collection.find_one({'_id': ObjectId(id)})
    if document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        return jsonify(document)
    else:
        return jsonify({'message': 'Document not found'}), 404

@app.route('/update/<id>', methods=['PUT'])
def update_document(id):
    document = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': document})
    if result.matched_count:
        return jsonify({'message': 'Document updated'})
    else:
        return jsonify({'message': 'Document not found'}), 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Document deleted'})
    else:
        return jsonify({'message': 'Document not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
