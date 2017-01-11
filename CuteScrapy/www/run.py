# coding:utf8
from flask import Flask, request
from flask.ext.restful import Api, Resource
from flask_restful_swagger import swagger


# app = Flask(__name__, static_folder='%sstatic' % FRONTEND_STATIC_PATH)
from CuteScrapy.model.blogs import Blogs
from CuteScrapy.www.response import HttpResponse

app = Flask(__name__)
# swagger
api = swagger.docs(Api(app), apiVersion='0.1.0', api_spec_url="/api/spec", description='博客爬虫')


class BlogList(Resource):
    @swagger.operation(
        summary='Blogs列表',
        parameters=[]
    )
    def get(self):
        data = Blogs().getBlogs()
        return HttpResponse.success(data)


api.add_resource(BlogList, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
