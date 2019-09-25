from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import numpy as np
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.path_ergodic import path_plan
bp = Blueprint('blog', __name__)
import json

@bp.route('/blog')
@login_required
def index():
    db = get_db()
    cu = db.cursor()
    va = cu.execute(
        'SELECT * FROM path_display'
    ).fetchall()
    display_num = va[-1][0] if va else 0
    vb = cu.execute(
        'SELECT * FROM path_transfer'
    ).fetchall()
    transfer_num = vb[-1][0] if vb else 0
    context = {
        'display_num':display_num,
        'transfer_num':transfer_num
    }
    return render_template('blog/index.html', **context)

@bp.route('/get_lite_data')
def get_lite_data():
    value = int(request.query_string.decode('utf-8').replace('%2C', '=').replace('&', '=').split('=')[-1])
    db = get_db()
    cu = db.cursor()
    va = cu.execute(
        # 'SELECT * FROM path_display'
        'SELECT * FROM path_transfer WHERE id={}'.format(value+1)
    ).fetchall()
    rlt_dict = {}
    rlt_dict['type'] = list(va[0])[3]
    rlt_dict['paths'] = {}
    for idx,i in enumerate(va):
        rlt_dict['paths'][idx] = [list(i)[1], list(i)[2]]
    # vb = [[list(i)[1], list(i)[2]] for i in va]
    data = jsonify(rlt_dict)
    return data

@bp.route('/save_path',methods=('GET', 'POST'))
def save_path(data=None):
    db = get_db()
    cu = db.cursor()
    va = cu.execute('SELECT * FROM path_transfer').fetchall()
    # get index
    if not va:
        num = 1
    else:
        num = max(np.array(va)[:,0])+1
    # save path coord
    if data:
        for i in data.values():
            db.execute('INSERT INTO path_transfer (id, x, y, attribute) VALUES (?, ?, ?, ?)',
                       (num, i[0], i[1], 2))
    else:
        data = request.query_string.decode('utf-8').replace('%2C', '=').replace('&', '=').split('=')[1:]
        # rlts = []

        for idx,i in enumerate(data):
            if idx % 2 == 0:
                # rlts.append([float(data[idx]),float(data[idx+1])])
                db.execute('INSERT INTO path_transfer (id, x, y, attribute) VALUES (?, ?, ?, ?)',
                   (num, float(data[idx]),float(data[idx+1]), 1))
    db.commit()
    return 'done'

@bp.route('/path_ergodic', methods=('GET', 'POST'))
def mystring():
    request_data = request.query_string.decode('utf-8').replace('%2C', '=').replace('&', '=').split('=')
    mid_x = float(request_data[1])
    mid_y = float(request_data[2])
    w = float(mid_x - float(request_data[4]))
    h = float(mid_y - float(request_data[5]))
    method = request_data[7]
    paths = path_plan(method,abs(int(w)), abs(int(h)))

    x = 1 if w == abs(w) else -1
    y = 1 if h == abs(h) else -1
    paths[:,0] = paths[:,0] * y + mid_x
    paths[:,1] = paths[:,1] * x + mid_y

    rlt_dict = {}
    for idx,i in enumerate(paths):
        rlt_dict[idx] = i.tolist()
    # save_path(rlt_dict)
    data = jsonify(rlt_dict)
    return data
