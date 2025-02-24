import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask,render_template,request,jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route ('/bucket', methods=['GET'])
def bucket_get():
    bucket_list = list (db.bucketlist.find ({}, {'_id':False}))

    return jsonify ({
        'buckets': bucket_list
    })

@app.route ('/bucket', methods=['POST'])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucketlist.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucketlist.insert_one(doc)
    
    return jsonify ({
        'msg': 'Your bucketlist was saved'
    })

@app.route ('/bucket/done', methods=['POST'])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucketlist.update_one(
        {'num':int(num_receive)}, 
        {'$set': {'done':1}}
    )
    return jsonify ({
        'msg':'update done!'
    })

@app.route('/delete', methods=['POST'])
def delete_item():
    num_receive = request.form['num_give']
    db.bucketlist.delete_one(
        {'num': int(num_receive)}
    )
    return jsonify({
        'msg': 'item deleted!'
    })

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)