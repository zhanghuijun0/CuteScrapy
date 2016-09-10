# coding:utf8
# 数据库引擎对象:

class DB():
    def update(self,sql,*args):
        print sql



if __name__ == '__main__':
    # orm = ORM()
    # orm.initTable()
    aa = DB()
    aa.update('sasdd','sa')