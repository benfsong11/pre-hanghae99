from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
app = Flask(__name__)


client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbsparta


# HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/memo/list', methods=['GET'])
def listing():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles': articles})


# API 역할을 하는 부분
@app.route('/memo/save', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdescription = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': ogtitle,
        'image': ogimage,
        'description': ogdescription,
        'url': url_receive,
        'comment': comment_receive
    }

    db.articles.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route('/memo/delete', methods=['POST'])
def deleting():
    url_receive = request.form['url_give']
    db.articles.delete_one({'url': url_receive})

    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
