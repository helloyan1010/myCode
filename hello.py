# -*- coding: utf-8 -*-
import web
from web import form
import psycopg2

render = web.template.render('template/') # your templates

db=web.database(dbn='postgres',user='postgres',pw='akefeifei',db='ppt')

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vname = form.regexp(r".{1,10}$", '名字长度不可为空，也不可超过10个字。')
##vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", vname, description="姓名"),
    form.Textbox("age",
                 form.notnull,
                 form.regexp('\d+', '必须是个整数。'),
                 form.Validator('必须大于10岁。', lambda x:int(x)>10),
                 description="年龄"),
    form.Dropdown("gender", [("F","女"),("M","男")],description="性别"),
    form.Dropdown("starsign",
                  [("摩羯座","摩羯座"),
                   ("水瓶座","水瓶座")],
                  description="星座"),
    form.Button("submit", type="submit", description="开始测试"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)


urls=(
    '/index','index'
      )

app=web.application(urls,globals())

class index:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.topk1st(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            return render.topk1st(f)
        else:
            return None;

if __name__=="__main__":
    web.internalerror=web.debugerror
    app.run()

