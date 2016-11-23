# coding:utf8
import json
import traceback

import math
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from CuteScrapy.model.blogs import Blogs

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

BASE_SUCCESS_RES = {
    'success': True,
    'code': 200,
    'message': 'success',
    'data': None
}

BASE_ERROR_RES = {
    'success': False,
    'code': -1,
    'message': 'error',
    'data': None
}


@app.route('/table', methods=['get'])
def table():
    site = request.args.get('site')
    page_str = request.args.get('page')
    pagesize_str = request.args.get('pagesize')
    try:
        page = int(page_str) if page_str is not None else 1
        pagesize = int(pagesize_str) if pagesize_str is not None else 20
        count = Blogs.getCountBySite(site)
        res = getSuccessResult(count, page, pagesize)
        data = Blogs.getBlobsBySite(site, page=page, pagesize=pagesize)
        res['data'] = []
        for msg in data:
            res['data'].append(msg.to_dict())
        pass
    except Exception, e:
        traceback.print_exc()
        res = BASE_ERROR_RES.copy()
        res['message'] = e.message
    return render_template('blogs.html', res=json.dumps(res.get('data')))


@app.route('/api', methods=['get'])
def getTest():
    site = request.args.get('site')
    page_str = request.args.get('page')
    pagesize_str = request.args.get('pagesize')
    try:
        page = int(page_str) if page_str is not None else 1
        pagesize = int(pagesize_str) if pagesize_str is not None else 20
        count = Blogs.getCountBySite(site)
        res = getSuccessResult(count, page, pagesize)
        data = Blogs.getBlobsBySite(site, page=page, pagesize=pagesize)
        res = []
        for msg in data:
            res.append(msg.to_dict())
        pass
    except Exception, e:
        traceback.print_exc()
        res = BASE_ERROR_RES.copy()
        res['message'] = e.message
    return json.dumps(res)


@app.route('/api/blogs', methods=['get'])
def getBlogs():
    site = request.args.get('site')
    page_str = request.args.get('page')
    pagesize_str = request.args.get('pagesize')
    try:
        page = int(page_str) if page_str is not None else 1
        pagesize = int(pagesize_str) if pagesize_str is not None else 20
        count = Blogs.getCountBySite(site)
        res = getSuccessResult(count, page, pagesize)
        data = Blogs.getBlobsBySite(site, page=page, pagesize=pagesize)
        res['data'] = []
        for msg in data:
            res['data'].append(msg.to_dict())
        pass
    except Exception, e:
        traceback.print_exc()
        res = BASE_ERROR_RES.copy()
        res['message'] = e.message
    return json.dumps(res)


@app.route('/', methods=['post', 'get'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/home', methods=['post', 'get'])
def home():
    blogs = Blogs()
    data = blogs.getAll()
    return render_template('list.html', data=data)


@app.route('/blogs', methods=['get'])
def blogs():
    blogs = Blogs()
    page = request.args.get('page')
    pagesize = request.args.get('pagesize')
    print page
    print pagesize
    if page and type(page) == int:
        data = blogs.getBlobsBySite(request.args.get('type'))

    data = blogs.getBlobsBySite(request.args.get('type'))
    return render_template('list.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def getSuccessResult(count, curr, pageSzie):
    res = BASE_SUCCESS_RES.copy()
    pageCount = math.ceil(count / float(pageSzie))
    if curr < 1:
        curr = 1
    elif curr > pageCount:
        curr = pageCount

    if pageCount == 1:
        pre = None
        next = None
    else:
        if curr == 1:
            pre = None
            next = curr + 1
        elif curr == pageCount:
            pre = curr - 1
            next = None
        else:
            pre = curr - 1
            next = curr + 1
    res['pre'] = pre
    res['next'] = next
    res['curr'] = curr
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
