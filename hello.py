# -*- coding: utf-8 -*-
import web
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from web import form
import psycopg2

render = web.template.render('template/') # your templates

db=web.database(dbn='postgres',user='postgres',pw='akefeifei',db='ppt')


##GLOBAL PARAM
global stu_id
stu_id=0
global page_no
page_no=1

##vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
##vname = form.regexp(r".{1,10}$", '名字长度不可为空，也不可超过10个字。')
####vemail = form.regexp(r".*@.*", "must be a valid email address")
##
##register_form = form.Form(
##    form.Textbox("username", vname, description="姓名"),
##    form.Textbox("age",
##                 form.regexp('\d+', '必须是个整数。'),
##                 form.Validator('必须大于10岁。', lambda x:int(x)>10),
##                 description="年龄"),
##    form.Dropdown("gender", [("F","女"),("M","男")],description="性别"),
##    form.Dropdown("starsign",
##                  [("摩羯座","摩羯座"),
##                   ("水瓶座","水瓶座"),
##                   ("双鱼座","双鱼座"),
##                   ("白羊座","白羊座"),
##                   ("金牛座","金牛座"),
##                   ("双子座","双子座"),
##                   ("巨蟹座","巨蟹座"),
##                   ("狮子座","狮子座"),
##                   ("处女座","处女座"),
##                   ("天秤座","天秤座"),
##                   ("天蝎座","天蝎座"),
##                   ("射手座","射手座")],
##                  description="星座"),
##    form.Button("Start",type="submit"),
##    
##)


urls=(
    '/list','list',
    '/index','index',
    '/result','result'
      )

app=web.application(urls,globals())

class index:
    def GET(self):
##        
##        f = register_form()
        return render.topk1st()

    def POST(self):
        
        global page_no,stu_id
        
        i=web.input()

        print i
        
        ## TODO: need to update with openId;
        selectvar=dict(name=i.get("username"))
        stus=db.select('students',selectvar,where="name=$name")
        counter=0
        
        for stu in stus:
            counter=counter+1
            stu_id=stu.id
            
        print( "the student counter is : %d" % (counter))
        
        if(counter==0):
            ## TODO: openId needed.
            stu_id=db.insert('students',name=i.get("username"),age=i.get("age"),
                    star_sign=i.get("starsign"),gender=i.get("gender"),area=i.get("area"))
            
            
            
            print("Insert STU id is: %d" % (stu_id))
            raise web.seeother('/list')
        else:
                scorevar=dict(sid=stu_id)
                scores=db.select('topk_score',scorevar,where="stu_id=$sid")
                counter1=0
                for score in scores:
                    counter1=counter1+1
                ## TODO: need update params
                if(counter1==0):
                    raise web.seeother('/list')
                else:
                    raise web.seeother('/result')
    

class list:
    def GET(self):
        global page_no
##        local_no=web.input()
##        page_no=int(local_no.get("no"))
##        ##itemsvar=dict(id=no.get("no"))
##        items=db.query('select * from items where id=$id',vars={'id':page_no})
##
##        ##TODO： why not itmes[0].id doesn'twork?
##        for item in items:
##            print(item)
##            print("items id:%s ,title:%s" % (item.id,item.title))
##            item=dict(no=item.id,title=item.title)
        return render.list()
        
    def POST(self):
        
        global page_no,stu_id
        
        i=web.input()
        print "****"
        print stu_id
        print "****"
        n=db.insert('topk_detail',stu_id=stu_id,item_score=i.get("answer"),
                    item_no=page_no)
        
        page_no=page_no+1
        
        print "****"
        print page_no
        print "****"
        string='/list?no='+str(page_no)
        raise web.seeother('/list')
    ##render.topk1st(f)

class result:
    def GET(self):
        return render.result()


if __name__=="__main__":
    web.internalerror=web.debugerror
    app.run()

