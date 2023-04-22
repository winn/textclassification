from flask import Flask, request, render_template,redirect, url_for, Response
from flask_cors import CORS
import requests
import json
from flask import jsonify
# from jinja2 import escape


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/generate_text', methods=['POST'])
def generate_text():
    # Get the input parameters from the request body

    # data = request.json
    data = json.loads(json.dumps(request.get_json()))
    print(data)
    # try:
    # return "ok"

    # print('hello')
    # return 'ok'
    # if isinstance(data, tuple):
    # # convert the tuple to a dictionary
    #     data = dict(data)
    prompt = data['prompt']
    model = data['model']
    apiKey = data['apiKey']
    max_tokens = int(data['maxToken'])


    # prompt = request.form['prompt']

    history = data['history']
    # history = []
    print(history)
    history = history[-300:]
    history = history.strip()

    # apiKey = request.form['apiKey']
    # model = request.form['model']
    # max_tokens = int(request.form['max_tokens'])



    apiUrl = 'https://api.openai.com/v1/chat/completions'

    history = history + ' user*' + prompt

    print(history)
    uList = history.split('end*')
    mList = []
    for u in uList:
        u = u.strip()
        usplit = u.split('user*')
        if len(usplit)>1:
            usplit = usplit[1]
            ssplit = usplit.split('system*')
            if len(ssplit)>1:
                umsg = ssplit[0]
                smsg = ssplit[1]
                udict = {}
                udict['role'] = 'user'
                udict['content'] = umsg
                mList.append(udict)
                sdict = {}
                sdict['role'] = 'system'
                sdict['content'] = smsg
                mList.append(sdict)
            else:
                udict = {}
                udict['role'] = 'user'
                udict['content'] = usplit
                mList.append(udict)


    data = {
        'model': model,
        'messages': mList,
        'max_tokens': max_tokens
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey
    }

    print(data)
    print(headers)
    # return "ok"

    response = requests.post(apiUrl, headers=headers, data=json.dumps(data))
    result = json.loads(response.content)

    res = {}
    res['answer'] = result['choices'][0]['message']
    history = history + ' system*' + res['answer']['content'] + ' end*'
    history = history[-300:]
    res['history'] = history
    print(res)
    return json.dumps(res)
    # except:
    #     return "ok"

if __name__ == '__main__':
    app.run(debug=True)
