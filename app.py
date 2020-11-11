from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)

client = MongoClient('mongodb://admin:admin@52.79.234.95:27017')
db = client.jungle

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
def get_memo():
    doc = db.memo.find()
    memo = json.loads(json_util.dumps(doc))
    return jsonify(memo)

@app.route('/memo/post', methods=['POST'])
def post_memo():
    form = request.form
    title = form['title']
    text = form['text']
    doc = {
        'title': title,
        'text': text
    }
    db.memo.insert_one(doc)
    return jsonify({'success': True, 'msg': '저장 완료!'})

@app.route('/memo/update', methods=['POST'])
def update_memo():
    form = request.form # form 구성: id, newTitle, newText
    self_id = form['id']
    new_title = form['newTitle']
    new_text = form['newText']
    db.memo.update_one({'_id': ObjectId(self_id)}, {
        '$set': {'title': new_title, 'text': new_text}
    })

    return jsonify({'success': True, 'msg': '수정 완료!'})

@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    form = request.form
    self_id = form['id']
    db.memo.delete_one({'_id': ObjectId(self_id)})
    return jsonify({'success': True, 'msg': '삭제 완료!'})

# localhost를 특정 ip로 변경할 것
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)