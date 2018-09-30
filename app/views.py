import datetime
import json
from io import BytesIO
from django.contrib import auth
from django import forms
from django.db.models import Q
from django.forms import fields
from django.forms import widgets
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User

from app import email_send
from app import models
from utils.check_code import create_validate_code
from utils.draw_image import draw_gragh
from utils.updateRelation import updateRelation
import random
import string


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = models.EmailVerifyRecord.objects.filter(code=active_code)

        if all_records:
            for record in all_records:
                email = record.email
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class AddCommentView(View):
    def post(self, request):
        print(request.POST)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['name', 'content', 'wlibrary']


class extendUser(forms.Form):
    # Login in interface, error_messages is the parameter of fields. If the username and password is null, prompt it. widget is the attributes of the input tag
    username = fields.CharField(error_messages={'required': 'Username is not null.'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "Please input Username"}))
    # For Passsword
    password = fields.CharField(error_messages={'required': 'Password is not null.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "Please input Password"}))


class Newuser(forms.Form):
    # register interface, Username is not more 9, not less 3, not null.
    username = fields.CharField(max_length=9, min_length=3,
                                error_messages={'required': 'Username is not null.',
                                                'max_length': 'Username is not more 9.',
                                                'min_length': 'Username is not less 3'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "Please input Username"}))
    email = fields.EmailField(
        error_messages={'required': 'Email address is not null', 'invalid': 'Email format is incorrect '},
        widget=widgets.Input(
            attrs={'type': "email", 'class': "form-control", 'name': "email", 'id': "email",
                   'placeholder': "Please enter your email address"}))

    # In the registration interface, the maximum length of password box is not more 12, the minimum cannot be less than 6, and cannot be null
    password = fields.CharField(max_length=12, min_length=6,
                                error_messages={'required': 'The password cannot be null.',
                                                'max_length': 'password is not more 12',
                                                'min_length': 'password is not less 6'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "Please input your password"})
                                )
    # In the registration interface, the maximum length of the password box can't be more than 9, and the content of the password box is compared with the previous one. The inconsistency of two times indicates "inconsistency of two passwords", and the minimum cannot be less than 3 and cannot be empty
    confirm_password = fields.CharField(max_length=12, min_length=6,
                                        error_messages={'required': 'not null.',
                                                        'max_length': 'The two passwords differ. ',
                                                        'min_length': 'The two passwords differ. '},
                                        widget=widgets.Input(
                                            attrs={'type': "password", 'class': "form-control",
                                                   'name': "confirm_password",
                                                   'id': "confirm_password",
                                                   'placeholder': "Please input the password"})
                                        )


def check_code(request):
    """
   verification code
    :param request:
    :return:
    """
    # stream = BytesIO()
    # img, code = create_validate_code()
    # img.save(stream, 'PNG')
    # request.session['CheckCode'] = code
    # return HttpResponse(stream.getvalue())

    # data = open('static/imgs/avatar/20130809170025.png','rb').read()
    # return HttpResponse(data)

    # 1. Create a picture pip3 install Pillow
    # 2. Write random strings in the image
    # obj = object ()
    # 3. Write the picture to the development file
    # 4.Open the make directory file and read the contents
    # 5. HttpResponse(data)

    stream = BytesIO()
    img, code = create_validate_code()
    # f=open('cc.png','wb')
    # img.save(f,'PNG')
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())
    # return HttpResponse(open('cc.png','rb').read())


def login(request):
    """
    login
    :param request:
    :return:
    """
    # if request.method == "POST":
    #     if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
    #         pass
    #     else:
    #         print('Verify code entered is wrong')
    er = ''
    s = ''
    if request.method == 'GET':
        obj = extendUser()
        return render(request, 'login.html', {'obj': obj})
    if request.method == 'POST':
        obj = extendUser(request.POST)
        code = request.POST.get('check_code')
        auto = request.POST.get('auto')
        if auto:
            request.session.set_expiry(2419200)
        else:
            pass
        if code.upper() == request.session['CheckCode'].upper():
            u = request.POST.get('username')
            t1 = User.objects.filter(username=u).values().first()
            if t1:
                pwd = request.POST.get('password')
                if auth.authenticate(username=u, password=pwd):
                    request.session['user'] = u
                    request.session['is_login'] = True
                    return redirect('/views/')
                else:
                    s = '''
                  <script>alert('Password error,Please re-type.');</script>
                  '''
            else:
                s = '''
           <script>alert('this username does not exist,Please check if it is correct.');</script>
                                '''

        else:
            er = 'Verify code entered is wrong.'
        return render(request, 'login.html', {'obj': obj, 'er': er, 's': s})


def nickname(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        print(nickname)
        u = request.session.get('user', None)
        user = User.objects.filter(username=u).values().first()
        models.UserProfile.objects.filter(user_id=user['id']).update(nickname=nickname)
    return HttpResponseRedirect('/my/')


def description(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        u = request.session.get('user', None)
        user = User.objects.filter(username=u).first()
        user.save()
        models.UserProfile.objects.filter(user_id=user.id).update(description=description)
    return HttpResponseRedirect('/my/')


def register(request):
    """
    register
    :param request:
    :return:
    """
    er = ''
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
        try:
            obj = Newuser(request.POST)
            r = obj.is_valid()
            if r:
                code = request.POST.get('check_code')
                if code.upper() == request.session['CheckCode'].upper():
                    user = request.POST.get('username')
                    email = request.POST.get('email')
                    nickname = ''.join(random.sample(string.ascii_letters + string.digits, 12))
                    thisUser = User.objects.filter(username=user).values().first()
                    thisNickname = models.UserProfile.objects.filter(nickname=nickname)
                    if thisUser:
                        s = '''
                    <script>alert('The username already exists, please input the username again!');
                    </script>
                        '''

                    elif thisUser and email == thisUser['email']:
                        s = '''
                    <script>alert('Email has been registered, please re-enter email!');
                    </script>
                    '''
                    elif thisNickname:
                        s = '''
                        <script>alert('The nickname already exists, please try again!');
                        </script>
                        '''
                    else:
                        pwd1 = request.POST.get('password')
                        pwd2 = request.POST.get('confirm_password')
                        if pwd1 != pwd2:
                            s = '''
                        <script>alert('Two passwords do not match, please check and re-enter!');</script>'''
                        else:
                            description = ''.join(random.sample(string.ascii_letters + string.digits, 12))
                            user1 = User.objects.create_user(username=user, password=pwd1, email=email)
                            user1.save()
                            models.UserProfile.objects.filter(user_id=user1.id).update(nickname=nickname,
                                                                                       description=description)
                            email_send.send_register_email(email, "register")
                            s = '''
                        <script>alert('registered successfully ');
                        </script>'''
                    return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
                else:
                    er = 'Verify code entered is wrong. '
                    return render(request, 'register.html', {'obj': obj, 'er': er})

            else:
                s = '''
            <script>alert('Incorrect information format, registration failed!');
                </script>'''
                return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
        except Exception as e:
            print(e)

            s = '''
           <script>alert('error, please try again.');</script>'''
            obj = Newuser()
            return render(request, 'register.html', {'s': s, 'obj': obj})


def views(request):
    u = request.session.get('user', None)
    if request.method == 'GET':
        operator = models.Operator.objects.filter().all().values()
        user = User.objects.filter(id=1).values()
        obj = None
        return render(request, 'views.html', {'obj': obj, 'u': u, 'operator': operator})
    elif request.method == 'POST':
        data = request.POST['content']
        data2 = request.POST['content2']
        if data2 == '':
            data2 = 'qwertyuiopasdg&*qwe'

        objs = models.Wlibrary.objects.filter(name__icontains=data)
        objs2 = models.Wlibrary.objects.filter(name__contains=data2)
        obj_list = []
        obj_list1 = [each.name for each in objs]
        obj_list2 = [each.name for each in objs2]
        if len(obj_list1) == 0:
            pass
        elif len(obj_list1) != 0 and len(obj_list2) == 0:
            for item1 in obj_list1:
                if (item1 in obj_list):
                    pass
                else:
                    obj_list.append(item1)
        elif len(obj_list1) != 0 and len(obj_list2) != 0:
            for item in obj_list1:
                for item2 in obj_list2:
                    if item != item2:
                        val = item + '&&' + item2
                        if (val in obj_list):
                            pass
                        else:
                            obj_list.append(val)
        res_dict = {
            "massage": "success",
            "code": 0,
            "successful": True,
            "data": obj_list
        }
        print(obj_list)
        return JsonResponse(res_dict)


def editTheorem(request):
    mcdc_tpye = ['omega', 'infinity']
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    error = ''
    if f:
        u_id = User.objects.filter(username=u).first().id
        user = User.objects.filter(username=u).first()
        userinfo = models.UserProfile.objects.filter(user_id=user.id).first()
        obj = models.Wlibrary.objects.filter(user_id=u_id)

    if request.method == 'GET':
        return render(request, 'my.html', {'obj': obj, 'u': user, 'u2': userinfo})
    if request.method == 'POST':
        t_name = request.POST.get('t_name', None)
        t_exp = request.POST.get('t_exp', None)
        t_ref = request.POST.get('t_ref', None)
        mcdc_1 = request.POST.get('mcdc1')
        mcdc_2 = request.POST.get('mcdc2')
        if t_name and t_exp and t_ref:
            if mcdc_1 not in mcdc_tpye and mcdc_1.isnumeric() == False:
                error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
            elif mcdc_2 not in mcdc_tpye and mcdc_2.isnumeric() == False:
                error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
            elif mcdc_1.isnumeric() and mcdc_1.isnumeric() and int(mcdc_1) >= int(mcdc_2):
                error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
            elif mcdc_1 in mcdc_tpye and mcdc_2.isnumeric() == True:
                error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
            elif mcdc_1 == 'omega' and mcdc_2 == 'omega':
                error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
            elif mcdc_1 == 'infinity' and mcdc_2 == 'omega':
                error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
            elif mcdc_1 == 'infinity' and mcdc_2 == 'infinity':
                error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
            else:
                models.Wlibrary.objects.filter(name=t_name).update(ref=t_ref, exp=t_exp, mcdc_1=mcdc_1, mcdc_2=mcdc_2)
                error = '''<script>alert('edit successfully！！！');</script>'''
        else:
            error = '''<script>alert('Please fill in all the information of the theorem！！！');</script>'''
        return render(request, 'my.html', {'u': u, 'u2': userinfo, 'obj': obj, 'error': error})


def add(request):
    mcdc_tpye = ['omega', 'infinity']
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    error = ''
    if f:
        if request.method == 'GET':
            return render(request, 'add.html', {'u': u, 'error': error})
        elif request.method == 'POST':
            t_name = request.POST.get('t_name', None)
            # t_label=request.POST.get('t_label',None)
            t_exp = request.POST.get('t_exp', None)
            t_ref = request.POST.get('t_ref', None)
            mcdc_1 = request.POST.get('mcdc1')
            mcdc_2 = request.POST.get('mcdc2')
            if t_name and t_exp and t_ref:
                if mcdc_1 not in mcdc_tpye and mcdc_1.isnumeric() == False:
                    error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
                elif mcdc_2 not in mcdc_tpye and mcdc_2.isnumeric() == False:
                    error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
                elif mcdc_1.isnumeric() and mcdc_1.isnumeric() and int(mcdc_1) >= int(mcdc_2):
                    error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
                elif mcdc_1 in mcdc_tpye and mcdc_2.isnumeric() == True:
                    error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
                elif mcdc_1 == 'omega' and mcdc_2 == 'omega':
                    error = '''<script>alert('Incorrect mcdc_2 format！！！');</script>'''
                elif mcdc_1 == 'infinity' and mcdc_2 == 'omega':
                    error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
                elif mcdc_1 == 'infinity' and mcdc_2 == 'infinity':
                    error = '''<script>alert('Incorrect mcdc_1 format！！！');</script>'''
                elif models.Wlibrary.objects.filter(name=t_name):
                    count = models.Wlibrary.objects.filter(name__contains=t_name).count()
                    t_name = t_name + '(' + str(count) + ')'
                    u_id = User.objects.filter(username=u).first().id
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    models.Wlibrary.objects.create(name=t_name, ref=t_ref, exp=t_exp, publish=time, user_id=u_id,
                                                   mcdc_1=mcdc_1, mcdc_2=mcdc_2)
                    # error = '''<script>alert('The theorem already exists!!!Can not be added repeatedly！！！');</script>'''
                    error = '''<script>alert('add successfully！！！');</script>'''
                else:
                    u_id = User.objects.filter(username=u).first().id
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    models.Wlibrary.objects.create(name=t_name, ref=t_ref, exp=t_exp, publish=time, user_id=u_id,
                                                   mcdc_1=mcdc_1, mcdc_2=mcdc_2)
                    error = '''<script>alert('add successfully！！！');</script>'''
            else:
                error = '''<script>alert('Please fill in all the information of the theorem！！！');</script>'''
            return render(request, 'add.html', {'u': u, 'error': error})
    else:
        obj = extendUser()
        return render(request, 'login.html', {'obj': obj})


def logout(request):
    request.session.clear()
    return render(request, 'views.html')


def my(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    if f:
        u_id = User.objects.filter(username=u).first().id
        user = User.objects.filter(username=u).first()
        userinfo = models.UserProfile.objects.filter(user_id=user.id).first()
        print(userinfo)
        obj = models.Wlibrary.objects.filter(user_id=u_id)
        return render(request, 'my.html', {'obj': obj, 'u': user, 'u2': userinfo})
    else:
        obj = extendUser()
        return render(request, 'login.html', {'obj': obj})


def add_r(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    obj = models.Wlibrary.objects.all()
    nexus = models.Nexus.objects.all()
    error = ''
    if f:
        user = User.objects.get(username=u)
        if request.method == 'GET':
            return render(request, 'add_r.html', {'u': u, 'obj': obj, 'error': error, 'nexus': nexus})
        elif request.method == 'POST':
            obj = models.Wlibrary.objects.all()
            t1 = request.POST.get('t1')
            t2 = request.POST.get('t2')
            t_ref = request.POST.get('t_ref')
            t_relation_exp = request.POST.get('t_relation_exp')
            t_relation_r = request.POST.get('t_relation')
            if t1 and t2 and t_relation_exp and t_relation_r:
                if t1 == t2:
                    error = '''<script>alert('You cannot select the same theorem to add a relation！！！');</script>'''
                else:
                    models.Relation2.objects.create(t11=t1, operator1='default', t12=0,
                                                    t21=t2, operator2='default', t22=0,
                                                    ref=t_ref, exp=t_relation_exp,
                                                    relationship_id=t_relation_r, user=user)
                    if int(t_relation_r) == 1:
                        obj1 = models.Wlibrary.objects.filter(id=t1).first()
                        obj2 = models.Wlibrary.objects.filter(id=t2).first()
                        updateRelation(obj1.name, obj2.name)
                    error = '''<script>alert('successfully added ！！！');</script>'''
            else:
                error = '''<script>alert('Relationships cannot be null');</script>'''
            return render(request, 'add_r.html', {'u': u, 'obj': obj, 'error': error, 'nexus': nexus})
    else:
        obj = extendUser()
        return render(request, 'login.html', {'obj': obj})


def add_r_operator(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    user = User.objects.get(username=u)
    operator = models.Operator.objects.filter().all().values()
    obj = models.Wlibrary.objects.all()
    nexus = models.Nexus.objects.all()
    error = ''
    if f:
        if request.method == 'GET':
            return render(request, 'add_r_operator.html',
                          {'u': u, 'obj': obj, 'error': error, 'nexus': nexus, 'operator': operator})
        elif request.method == 'POST':
            t11 = request.POST.get('t1')
            operator1 = request.POST.get('operator')
            t12 = request.POST.get('t1_2')
            t21 = request.POST.get('t2')
            operator2 = request.POST.get('operator2')
            t22 = request.POST.get('t2_2')
            t_ref = request.POST.get('t_ref')
            t_relation_exp = request.POST.get('t_relation_exp')
            t_relation_r = request.POST.get('t_relation')

            if t11 and t21 and t_relation_exp and t_relation_r:
                if operator1 == 'default' and operator2 == 'default':
                    error = '''<script>alert('At least one operator not be default ！！！');</script>'''
                else:
                    models.Relation2.objects.create(t11=t11, operator1=operator1, t12=t12,
                                                    relationship_id=t_relation_r, exp=t_relation_exp,
                                                    t21=t21, operator2=operator2, t22=t22, user=user)
                    error = '''<script>alert('successfully added ！！！');</script>'''
            else:
                error = '''<script>alert('Relationships cannot be null');</script>'''
            return render(request, 'add_r_operator.html',
                          {'u': u, 'obj': obj, 'error': error, 'nexus': nexus, 'operator': operator})
    else:
        obj = extendUser()
        return render(request, 'login.html', {'obj': obj})


def detail(request):
    u = request.session.get('user', None)
    title = request.path
    t = title[7:-1]
    obj = models.Wlibrary.objects.filter(name=t).first()
    comments = models.Comment.objects.filter(wlibrary=obj).all()
    count = models.Comment.objects.filter(wlibrary=obj).count()
    return render(request, 'detail.html', {'obj': obj, 'u': u, 'comments': comments, 'comment_nums': count})


def users(request):
    u = request.session.get('user', None)
    operator1 = ('*', '◇', '~')
    operator2 = ('∪', '∩', '✱', 'ㄨ')
    if request.method == 'GET':
        content = request.GET.get('user', None)
        if content and content != '':
            ret = {'status': True, 'data': None, 'error': None, 'data2': None, 'exp': None, 'type': None,
                   'relations': True}
            aim = User.objects.filter(username__icontains=content).first()
            if aim:
                datas = []
                datas2 = []
                exps = []
                types = []
                objs = models.Relation2.objects.filter(user_id=aim.id)

                if objs:
                    print(len(objs))
                    for row in objs:
                        obj11 = models.Wlibrary.objects.filter(id=row.t11).values('id', 'name').first()
                        oper1 = '' if row.operator1 == 'default' else row.operator1
                        t1 = obj11['name'] + oper1
                        obj12 = models.Wlibrary.objects.filter(id=row.t12).values().first()
                        if obj12 != None:
                            t1 += obj12['name']
                        obj21 = models.Wlibrary.objects.filter(id=row.t21).values().first()
                        oper2 = '' if row.operator2 == 'default' else row.operator2
                        try:
                            t2 = obj21['name'] + oper2
                        except:
                            t2 = oper2
                        obj22 = models.Wlibrary.objects.filter(id=row.t22).values().first()
                        if obj22 != None:
                            t2 += obj22['name']
                        if t1 in datas and t2 in datas2 and row.exp in exps:
                            pass
                        else:
                            datas.append(t1)
                            datas2.append(t2)
                            exps.append(row.exp)
                            types.append(row.relationship.id)
                    ret['exp'] = json.dumps(exps)
                    ret['data'] = datas
                    ret['data2'] = datas2
                    ret['type'] = json.dumps(types)
                    if ret['data'] == None:
                        ret['relations'] = False
                        for row in aim:
                            datas.append(row.name)
                        ret['data'] = datas
                else:
                    ret['status'] = False
                    ret['error'] = 'This user has not published the relevant theorem！！！'
            else:
                obj = None
                ret['status'] = False
                ret['error'] = 'No relevant distributors were found！！！'
            return render(request, 'user_2.html', ret)
        else:
            obj = None
            return render(request, 'view_users.html', {'obj': obj, 'u': u})
    elif request.method == 'POST':
        ret = {"status": True, "data": None, "error": None, "relations": True}
        content = request.POST.get('content', None)
        if content and content != '':
            aim = User.objects.filter(username__contains=content)
            if aim:
                datas = []
                for row in aim:
                    datas.append(row.username)
                ret['data'] = datas
            else:
                obj = None
                ret['status'] = False
                ret['error'] = 'No relevant distributors were found！！！'

                # if aim:
                #     datas = []
                #     datas2 = []
                #     exps = []
                #     types = []
                #     objs = models.Relation2.objects.filter(user_id= aim.id)
                #     if objs:
                #         print(len(objs))
                #         for row in objs:
                #             obj11 = models.Wlibrary.objects.filter(id = row.t11).values('id','name').first()
                #             oper1 = '' if row.operator1 == 'default' else row.operator1
                #             t1 = obj11['name'] + oper1
                #             obj12 = models.Wlibrary.objects.filter(id=row.t12).values().first()
                #             if obj12 != None:
                #                 t1 += obj12['name']
                #             obj21 = models.Wlibrary.objects.filter(id=row.t21).values().first()
                #             oper2 = '' if row.operator2 == 'default' else row.operator2
                #             t2 = obj21['name'] + oper2
                #             obj22 = models.Wlibrary.objects.filter(id=row.t22).values().first()
                #             if obj22 != None:
                #                 t2 += obj22['name']
                #             if t1 in datas and t2 in datas2 and row.exp in exps:
                #                 pass
                #             else:
                #                 datas.append(t1)
                #                 datas2.append(t2)
                #                 exps.append(row.exp)
                #                 types.append(row.relationship.id)
                #         ret['exp'] = json.dumps(exps)
                #         ret['data'] = json.dumps(datas)
                #         ret['data2'] = json.dumps(datas2)
                #         ret['type'] = json.dumps(types)
                #         if ret['data'] == None:
                #             ret['relations'] = False
                #             for row in aim:
                #                 datas.append(row.name)
                #             ret['data'] = json.dumps(datas)
                #     else:
                #         ret['status'] = False
                #         ret['error'] = 'This user has not published the relevant theorem！！！'
                # else:
                #     obj = None
                #     ret['status'] = False
                #     ret['error'] = 'No relevant distributors were found！！！'

        return HttpResponse(json.dumps(ret))


def draw_image(request):
    u = request.session.get('user', None) or "guest"
    data = request.POST['data']
    data_array = json.loads(data)
    import base64
    r_list = draw_gragh(data_array, u)
    with open(u + '.png', 'rb') as f:  # Open the diagram file in binary mode
        ls_f = base64.b64encode(f.read())  # reads the file content and converts it into base64 encoding
    res_dict = {
        "massage": "success",
        "code": 0,
        "successful": True,
        "data": {
            "image": str(ls_f, encoding='ascii'),
            "relation": r_list
        }
    }
    return JsonResponse(res_dict)


def relation(request):
    id = int(request.GET['id'])
    r = models.Relation2.objects.get(id=id)
    t11 = models.Wlibrary.objects.get(id=r.t11)
    oper1 = '' if r.operator1 == 'default' else r.operator1
    t1 = t11.name + oper1
    t12 = models.Wlibrary.objects.filter(id=r.t12).first()
    if t12:
        t1 += t12.name
    t21 = models.Wlibrary.objects.get(id=r.t21)
    oper2 = '' if r.operator2 == 'default' else r.operator2
    t2 = t21.name + oper2
    t22 = models.Wlibrary.objects.filter(id=r.t22).first()
    if t22:
        t2 += t22.name
    users = models.UserProfile.objects.filter(user_id=r.user_id).values().first()
    nickname = users['nickname']
    res = {
        "t1": t1,
        "t2": t2,
        "l_name_r": r.relationship.r_name,
        "l_name_exp": r.exp,
        "ref": r.ref,
        "username": nickname,
    }
    return render(request, 'relation.html', res)


def resetPassword(request):
    try:
        obj = extendUser()
        if request.method == "GET":
            return render(request, 'resetPassword.html', {'obj': obj})
        if request.method == "POST":
            un = request.POST.get('username')
            pw = request.POST.get('password')
            print(un, pw)
            user = User.objects.get(username=un)
            if user == None:
                er = 'this username is not exist'
            else:
                user.set_password(pw)
                user.save()
                er = "success"
            return render(request, 'resetPassword.html', {'er': er, 'obj': obj})
    except:
        return render(request, 'resetPassword.html', {'er': 'err', 'obj': obj})


def notfound(request):
    return redirect('/login/')
