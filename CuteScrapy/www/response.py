class HttpResponse():
    @classmethod
    def success(cls, data={}):
        return {
            'code': 200,
            'success': True,
            'msg': 'success',
            'data': data
        }

    @classmethod
    def error(cls, data={}, error_code=-1, msg='error'):
        return {
            'code': error_code,
            'success': False,
            'msg': msg,
            'data': data
        }
