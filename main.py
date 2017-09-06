# -*- coding: utf-8 -*-
import web
import sys
from web import form
import psycopg2

##ONLY Needed on linux
##reload(sys)
##sys.setdefaultencoding('utf8')

render = web.template.render('template/') # your templates

db=web.database(dbn='postgres',user='postgres',pw='akefeifei',db='ppt')

urls = (
    '/wx', 'index',
)



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

class index:
    def GET(self):
        
        selectvar=dict(type=4)
        f=db.select('mainreason',selectvar,where="type=$type")
        return render.test(f)    

