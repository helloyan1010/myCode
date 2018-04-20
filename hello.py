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
global lists
lists=[]

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
        
        global stu_id,list_value, reason1_value,topk_result
        
        i=web.input()
        
        print "****show the character type from last page.****"
        print list_value
        print "****"
        
        selectvar=dict(char_type=list_value)
        reason_list=db.select('reason_list',selectvar,where="char_type=$char_type")
        return render.mainreason(reason_list)
        
    def POST(self):
        
        global stu_id,list_value, reason1_value,topk_result

        ## should shown the result 
        i=web.input()
        reason1_value=int(i.get("reasonAnswer")) 
        
        print "****print the main reason id: ******"
        print reason1_value
        print "****"

        ##get TOPK result from reason id.
        topk_results=db.query('select topk_result from reason_list where id=$id',vars={'id':reason1_value})
        for item in topk_results:
            topk_result=item.topk_result
            print("TOPK result is: %s" %(topk_result))
        
        ##
        
        ##INSERT DB
        
        selectvar=dict(id=stu_id)
        score_results=db.select('topk_score',selectvar,where="stu_id=$id")

        counter=0        
        for detail in score_results:
            counter=counter+1
            
        print( "the topk score counter is : %d" % (counter))
        
        if(counter==0):
             ## TODO: openId needed.
            score_id=db.insert('topk_score',stu_id=stu_id,topk_result=topk_result,reason_id=reason1_value)
            
            print("Insert topk_score successfullly! stu_id is: %d" % (stu_id))
        else:            
            score_id=db.update('topk_score',where="stu_id=$id",vars={'id':stu_id},topk_result=topk_result,reason_id=reason1_value)
            
            print("update topk_detail successfully! stu)id is: %d" % (stu_id))

        
                
        ## END

        
        raise web.seeother('/result')

class result:
    def GET(self):
        
        global stu_id,list_value, reason1_value,topk_result,lists

        lists=[]
        print "****print the topk result: ******"
        print topk_result
        print "****"

        if(stu_id!=0):
            for ch in topk_result:
                result_items=db.query('select * from topk_type where short=$short',vars={'short':ch})
                for item in result_items:
                    lists.append(item)
                    print item.short
                    print item.long
                    print item.description
            return render.result(topk_result,lists)
        else:
            return "Error: No such person."
     


if __name__=="__main__":
    web.internalerror=web.debugerror
    app.run()

