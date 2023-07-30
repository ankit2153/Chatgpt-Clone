from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

import openai

openai.api_key = "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"


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/chatgpt"

mongo = PyMongo(app)


@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    print(mychats)
    return render_template("index.html", mychats=mychats)


@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")

        chat = mongo.db.chats.find_one({"question": question})

        print(chat)

        if chat:
            data = {"result": {chat['answer']}}
            return jsonify(data)
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            print(response['choices'][0]['message']['content'])

            mongo.db.chats.insert_one({"question": question,"answer":response['choices'][0]['message']['content'] })
            data = {"question": question,"answer":response['choices'][0]['message']['content']}
            return jsonify(data)

    data = {"result": "this is the first result of my chatgpt clone"}
    return jsonify(data)


app.run(debug=True)
