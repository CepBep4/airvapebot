from flask import Flask, render_template, jsonify, request, abort
from urls import urls, urls_admin
from dbcontrol import base_get, base_get_all, base_edit , base_add
import json
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return jsonify(urls)

@app.route('/admin/api')
def api_admin():
    return render_template('home.html')

@app.route('/api/<req>', methods=['GET','POST'])
def api_get(req):
    if request.method == "POST":
        if not list(request.args.lists()):
            response = base_add(req,json.loads(request.data))
            
            if not isinstance(response, bool):
                return jsonify([{'success': True}, 200])
            else:
                return abort(500, response[1])
        else:
            key, val = list(request.args.lists())[0]
            response = base_edit(req, key, val[0], json.loads(request.data))            
            
            if isinstance(response, bool):
                return jsonify([{'success': True}, 200])
            else:
                abort(500, response[1])
    else:
        if list(request.args.lists()):
            key, val = list(request.args.lists())[0]
            data = base_get(req, key, val[0])
            
            if not isinstance(data, tuple):
                return jsonify(data)
            else:
                return abort(500, data[1])
        else:
            return jsonify(base_get_all(req))
        
@app.route('/api/open')
def open_case():
    key, val = list(request.args.lists())[0]
    case = base_get('case', key, val[0])
    val_ruffle = randint(0,100)
    chances = []
    item_win = None
    
    for index,item in  enumerate(list(case['chance'])):
        if index != 0:
            chances.append(case['chance'][item]+chances[index-1])
        else:
            chances.append(case['chance'][item])

    for index,chancse in enumerate(chances):
        if index != 0:
            if val_ruffle >= chances[index-1] and val_ruffle <= chancse:
                item_win = list(case['chance'])[index]
        else:
            if val_ruffle >= 0 and val_ruffle <= chancse:
                item_win = list(case['chance'])[index]    
    
    base_add('history', {
        'id':0,
        'case_id':case['id'],
        'number_raffle': len(base_get_all('history')),
        'prize':item_win
    })
    
    return jsonify(
        {
            'case_id':case['id'],
            'win_item':item_win,
            'number_raffle':len(base_get_all('history')),
            'case_info_for_user':{'case_id':case['id'], 'win_item':item_win, 'number_raffle':len(base_get_all('history'))}
        }
    )
    
@app.route('/api/first_open')
def open_case_first():
    key, val = list(request.args.lists())[0]
    case = base_get('case', key, val[0])
    chances = []
    item_win = ''
    
    for index,item in  enumerate(list(case['chance'])):
        if index != 0:
            chances.append(case['chance'][item]+chances[index-1])
        else:
            chances.append(case['chance'][item])

    count_while = 0

    while 'sale' not in item_win:
        val_ruffle = randint(0,100)
        for index,chancse in enumerate(chances):
            if index != 0:
                if val_ruffle >= chances[index-1] and val_ruffle <= chancse:
                    item_win = list(case['chance'])[index]
            else:
                if val_ruffle >= 0 and val_ruffle <= chancse:
                    item_win = list(case['chance'])[index]    
    
    base_add('history', {
        'id':0,
        'case_id':case['id'],
        'number_raffle': len(base_get_all('history')),
        'prize':item_win
    })
    
    return jsonify(
        {
            'case_id':case['id'],
            'win_item':item_win,
            'number_raffle':len(base_get_all('history')),
            'case_info_for_user':{'case_id':case['id'], 'win_item':item_win, 'number_raffle':len(base_get_all('history'))}
        }
    )
    
@app.after_request
def allow_anyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response