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


##GLOBAL PARAM
global stu_id
stu_id=1
global list_value
list_value=0
global reason1_value
reason1_value=0


urls=(
    '/list','list',
    '/index','index',
    '/mainreason','mainreason',
    '/result','result',
      )

app=web.application(urls,globals())

class index:
    def GET(self):
        return render.topk1st()

    def POST(self):
        
        global stu_id
        
        i=web.input()

        print i
        
        ## TODO: need to update with openId;
        ## Get user Info here ,to determine which page should be shown:
        ## counter=0:insert a new user
        ## counter!=0: if test not finished last time, go ahead to finish.else, shown the result.
        ##
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
        return render.list()
        
    def POST(self):
        
        global stu_id,list_value, reason1_value
        
        i=web.input()
        list_value=int(i.get("answer"))
        
        print "****"
        print ("STU id is: %d" % (stu_id))
        print "****"
        
        print "****"
        print list_value
        print "****"
        
        raise web.seeother('/mainreason')

class mainreason:
    def GET(self):
        
        global stu_id,list_value, reason1_value
        
        i=web.input()
        
        print "****"
        print list_value
        print "****"
        
        selectvar=dict(topk_type=list_value)
        reason_list=db.select('reason_list',selectvar,where="topk_type=$topk_type")
        return render.mainreason(reason_list)
        
    def POST(self):
        
        global stu_id,list_value, reason1_value

        ## should shown the result 
        i=web.input()
        reason1_value=int(i.get("answer")) 
        
        print "****"
        print reason1_value
        print "****"
        
        ##INSERT DB
        
        selectvar=dict(id=stu_id)
        detail_results=db.select('topk_detail',selectvar,where="stu_id=$id")

        counter=0        
        for detail in detail_results:
            counter=counter+1
            
        print( "the topk detail counter is : %d" % (counter))
        
        if(counter==0):
             ## TODO: openId needed.
            detail_id=db.insert('topk_detail',stu_id=stu_id,role_id=list_value,reason_id=reason1_value)
            
            print("Insert topk_detail id is: %d" % (stu_id))
        else:            
            detail_id=db.update('topk_detail',where="stu_id=$id",vars={'id':stu_id},role_id=list_value,reason_id=reason1_value)
            
            print("update topk_detail id is: %d" % (stu_id))

        
        ## 判断类型
        first_type=0
        second_type=0
        third_type=0

        if(list_value==4 ):
            first_type=1
            if(reason1_value==1):
                second_type=2
            else:
                second_type=3

        if(list_value==5):
            first_type=3
            
        if(list_value==3):
            first_type=2
            
        if(list_value==2):
            first_type=4
            
        if(list_value==1):
            first_type=4

        
                
        ## END

        score_results=db.query('select * from topk_score where stu_id=$id',vars={'id':stu_id})

        counter=0
        for score in score_results:
            counter=counter+1

        if(counter==0):
            score_result=db.insert('topk_score',stu_id=stu_id,first_type=first_type,second_type=second_type,third_type=third_type)
        else:            
            score_result=db.update('topk_score',where="stu_id=$id",vars={'id':stu_id},first_type=first_type,second_type=second_type,third_type=third_type)
        
        
        raise web.seeother('/result')

class result:
    def GET(self):
        
        global stu_id,list_value, reason1_value

        if(stu_id!=0):
            
            score_results=db.query('select * from topk_score where stu_id=$id',vars={'id':stu_id})

            for score_result in score_results:
                first=db.query('select * from topk_type where id=$id',vars={'id':score_result.first_type})
                second=db.query('select * from topk_type where id=$id',vars={'id':score_result.second_type})
                third=db.query('select * from topk_type where id=$id',vars={'id':score_result.third_type})

                return render.result(first,second,third)
        else:
            return "ERROR: 没有查询到这个人."


if __name__=="__main__":
    web.internalerror=web.debugerror
    app.run()

