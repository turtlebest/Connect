from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages
import spoontifylib.SFDBManager
import spoontifylib.SFUtil
import sys
import os
import uuid
import shutil
# Create your views here.

from .forms import SignUpForm
from .models import Document
from .forms import DocumentForm
from django.conf import settings

def handle_uploaded_file(f, username):
    #with open(f.name, 'wb+') as destination:
    path = "%s/documents/%s/" % (settings.MEDIA_ROOT, username)
    if not os.path.exists (path): 
      os.makedirs(path)
    
    filepath = path + f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)    

def handle_uploaded_Pfile(f, username):
    #with open(f.name, 'wb+') as destination:
    path = "%s/user/%s/" % (settings.MEDIA_ROOT, username)
    if not os.path.exists (path): 
      os.makedirs(path)
    
    filepath = path + f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)    



def home(request):

    if request.POST:

      print("TTT") 
      raw_username = request.POST.get('username_input')
      raw_password = request.POST.get('password_input')	  
      username = raw_username.strip()
      password = raw_password.strip()       
      print(password) 
      print(username) # this was just for me to check
      
      sf_db = spoontifylib.SFDBManager.SFDBManager()
      login_check_sentence = """SELECT pwd FROM User_Info Where uid = %s"""
      login_set = [username]
      check_login_password = sf_db.query_data(login_check_sentence,login_set)

      if not check_login_password:
          messages.success(request, 'no user existed.')
          return HttpResponseRedirect('/index')
      elif password != check_login_password[0][0]:
          messages.success(request, 'Wrong password.')
          return HttpResponseRedirect("/index")
      else:
          request.session['username'] = username
          request.session['is_login'] = True
          return HttpResponseRedirect("/main")

      print(check_login_password) 

      show_info = {}
      #show_info['show_info'] = ''
      show_info['is_login'] = 'true'
      return HttpResponseRedirect('/main')
        

    form = SignUpForm(request.POST or None)
    
    if form.is_valid():
        save_it = form.save(commit = False)
        save_it.save()
        messages.success(request, 'Thank you for joining')
        return HttpResponseRedirect('/thank-you')
    
  
    
    return render_to_response("signup.html",
                              locals(),
                              context_instance = RequestContext(request))

def thankyou(request):

    return render_to_response("thankyou.html",
                              locals(),
                              context_instance = RequestContext(request))    


def aboutus(request):
        
    return render_to_response("aboutus.html",
                              locals(),
                              context_instance = RequestContext(request))

def main(request):
   if request.method == 'POST':
      information = request.POST.get('information_post_input')
      form = DocumentForm(request.POST, request.FILES)
      print("AA")
      print form 
      if form.is_valid():
        username = request.session['username']
        handle_uploaded_file(request.FILES['docfile'], username)
        print(request.FILES['docfile'].name)
        
        path = "http://127.0.0.1:8000/media/documents/%s/" % (username)
        filepath = path + request.FILES['docfile'].name
        PostType = 1
        text = ""
        caption = information
      else:
        filepath = None  
        PostType = 0
        text = information
        caption = ""
      
      if request.POST.get('circle') == 'public' or request.POST.get('circle') == 'friends' or request.POST.get('circle') == 'privacy':
        circle = ""
        Visible = request.POST.get('circle')
      else:
        circle = request.POST.get('circle')
        Visible = ""
      location = request.POST.get('location_input')

      pid = os.urandom(16)
      lid = os.urandom(16)
      print(pid)

      sf_db = spoontifylib.SFDBManager.SFDBManager()
      insert_post_location_sentence = "INSERT INTO Location VALUES(%s,%s,0,0,NULL,NULL)"
      insert_post_location_sentence_list = [lid,location]
      sf_db.execute_sql(insert_post_location_sentence, insert_post_location_sentence_list)

      post_insert_sentence = """INSERT INTO Post VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)"""
      post_info_list = [pid,request.session['username'],location,PostType,Visible,circle,filepath,text,caption]
      sf_db.execute_sql(post_insert_sentence, post_info_list)

      return HttpResponseRedirect('/main')
   else:
      form = DocumentForm()

   show_info = {'form': form}
   show_info['is_login'] = 'true'
   
   get_all_post_text_sentence = """SELECT distinct P.uid, P.text, u.uname, u.URL,P.lid FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and (P.type=0) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'friends') or (P.Visible='private'and P.uid = %s)or(P.uid = %s)) ORDER BY P.date desc"""
   get_all_post_photoandcap_sentence = """SELECT distinct  P.uid, P.URL,P.caption, u.uname, u.URL, P.lid FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and (P.type=1) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'public') or (P.Visible='private'and P.uid = %s) or(P.uid = %s)) ORDER BY P.date desc"""
   
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   
   update_all_text_list = [request.session['username'],request.session['username'],request.session['username']]
   all_post_text_info = sf_db.query_data(get_all_post_text_sentence,update_all_text_list)
   all_post_photoandcap_info = sf_db.query_data(get_all_post_photoandcap_sentence,update_all_text_list)

   getname_sentence = """SELECT uname FROM User_Info Where uid = %s"""
   getname_set = request.session['username']
   uname = sf_db.query_data(getname_sentence, getname_set)

   get_location_sentence = """SELECT name FROM Location """
   location_list = sf_db.query_data(get_location_sentence)

   sf_db = spoontifylib.SFDBManager.SFDBManager()
   get_circle_list_sentence = """SELECT a.cname FROM CirclePeople as c, Circle as a Where c.cid = a.cid and c.uid = %s and c.IsOwner = 1"""
   update_circle_list = request.session['username']
   own_circle = sf_db.query_data(get_circle_list_sentence, "Jessica0725")
   print("aa:%s", update_circle_list)
   
   update_circle_list_Fix = {}
   update_circle_list_Fix[0] = "public"
   update_circle_list_Fix[1] = "frineds"
   update_circle_list_Fix[2] = "private"

   for index in range(len(own_circle)):
     update_circle_list_Fix[3+index] = own_circle[index][0]

   show_info['list_circle'] = own_circle 
   print update_circle_list_Fix

   show_info['textinfo'] = all_post_text_info
   show_info['photoinfo'] = all_post_photoandcap_info
   show_info['location_list'] = location_list
   show_info['userid'] = request.session['username']
   show_info['uname'] = uname[0][0]


   return render_to_response("main.html",
                              show_info,
                           context_instance = RequestContext(request))
  
def profile(request):
   show_info = {}
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   show_info['username'] = request.session['username']
  
   get_all_info_sentence = "SELECT uname,uid, profile, URL FROM User_Info where uid = %s"
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   all_info = sf_db.query_data(get_all_info_sentence,request.session['username'])

   get_all_post_text_sentence = """SELECT distinct P.uid, P.text, u.uname,u.URL,P.lid FROM Post as P, User_Info as u WHERE u.uid = P.uid and (P.type=0) and P.uid = %s ORDER BY P.date desc"""
   get_all_post_photoandcap_sentence = """SELECT distinct  P.uid, P.URL,P.caption,u.uname ,u.URL,P.lid FROM Post as P ,User_Info as u WHERE u.uid = P.uid and (P.type=1) and P.uid = %s ORDER BY P.date desc"""
    
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   #update_all_text_list = [searchText,request.session['username'],request.session['username'],request.session['username']]
   all_post_text_info = sf_db.query_data(get_all_post_text_sentence,request.session['username'])
   all_post_photoandcap_info = sf_db.query_data(get_all_post_photoandcap_sentence,request.session['username'])


   #get_location_info_sentence = "SELECT L.name FROM Location as L, User_Info as U WHERE U.lid = L.lid and U.uid = %s "
   get_location_info_sentence = "SELECT lid FROM User_Info where uid = %s"
   profile_map_location_name = sf_db.query_data(get_location_info_sentence,request.session['username'])
   
   show_info['location'] = profile_map_location_name
   show_info['name'] = all_info[0][0]
   show_info['uid'] = all_info[0][1]
   show_info['profile'] = all_info[0][2]
   show_info['url'] = all_info[0][3]
   show_info['textinfo'] = all_post_text_info
   show_info['photoinfo'] = all_post_photoandcap_info


   return render_to_response('profile.html', show_info, context_instance = RequestContext(request))
  
def edit_profile(request):
   form = DocumentForm()
   if request.POST:
      show_info = {}
      form = DocumentForm(request.POST, request.FILES)
      rst_pwd = request.POST.get('resetpw_input')
      confirm_pwd = request.POST.get('confirmpw_input')
      username = request.POST.get('user_name_input')
      descri = request.POST.get('description')
      location = request.POST.get('location')
      print location
      filepath = ""

      sf_db = spoontifylib.SFDBManager.SFDBManager()   

      
      # update pwd
      if rst_pwd==confirm_pwd!='':
        rst_pwd_sentence="""UPDATE User_Info SET pwd=%s Where uid = %s"""
        update_pwd_list = [rst_pwd,request.session['username']]
        sf_db.execute_sql(rst_pwd_sentence, update_pwd_list)

        if username != '':
          rst_username_sentence = """ UPDATE User_Info SET uname = %s Where uid = %s """
          update_uname_list = [username,request.session['username']]
          sf_db.execute_sql(rst_username_sentence, update_uname_list)
        else:
          print("uname do not change")

        if descri != '':
          rst_descri_sentence = """ UPDATE User_Info SET profile = %s Where uid = %s """
          update_descri_list = [descri,request.session['username']]
          sf_db.execute_sql(rst_descri_sentence, update_descri_list)
        else:
          print("description do not change0")
        if location !='':
            rst_location_sentence = "UPDATE User_Info SET lid = %s where uid = %s"
            update_location_list = [location,request.session['username']]
            sf_db.execute_sql(rst_location_sentence, update_location_list)
        else:
          print("location do not change")

        if form.is_valid():
          print("PIC")
          username = request.session['username']
          handle_uploaded_Pfile(request.FILES['docfile'], username)
          print(request.FILES['docfile'].name)
        
          path = "http://127.0.0.1:8000/media/user/%s/" % (username)
          filepath = path + request.FILES['docfile'].name

          rst_pwd_sentence="""UPDATE User_Info SET URL=%s Where uid = %s"""
          update_pwd_list = [filepath,request.session['username']]
          sf_db.execute_sql(rst_pwd_sentence, update_pwd_list)  

      elif rst_pwd==confirm_pwd=='':
        print("not change pwd")
        if username != '':
          rst_username_sentence = """ UPDATE User_Info SET uname = %s Where uid = %s """
          update_uname_list = [username,request.session['username']]
          sf_db.execute_sql(rst_username_sentence, update_uname_list)
        else:
          print("uname do not change") 

        if descri != '':
          rst_descri_sentence = """ UPDATE User_Info SET profile = %s Where uid = %s """
          update_descri_list = [descri,request.session['username']]
          sf_db.execute_sql(rst_descri_sentence, update_descri_list)
        else:
          print("description do not change1")
        
        if location !='':
            rst_location_sentence = "UPDATE User_Info SET lid = %s where uid = %s"
            update_location_list = [location,request.session['username']]
            sf_db.execute_sql(rst_location_sentence, update_location_list)
        else:
          print("location do not change")

        if form.is_valid():
          print("PIC")
          username = request.session['username']
          handle_uploaded_Pfile(request.FILES['docfile'], username)
          print(request.FILES['docfile'].name)
        
          path = "http://127.0.0.1:8000/media/user/%s/" % (username)
          filepath = path + request.FILES['docfile'].name

          rst_pwd_sentence="""UPDATE User_Info SET URL=%s Where uid = %s"""
          update_pwd_list = [filepath,request.session['username']]
          sf_db.execute_sql(rst_pwd_sentence, update_pwd_list)  
      else:
        print("please enter again pwd")

      

      #show_info['show_info'] = ''
      show_info['is_login'] = 'true'
      return HttpResponseRedirect('/profile')
      #return render_to_response('profile.html', show_info)
    
   
   show_info = {'form': form}      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   return render_to_response('edit_profile.html', show_info, context_instance = RequestContext(request)) 

def friend_profile(request, target_username=''):
   if request.method == 'post1':
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     friend_request_setence = "INSERT INTO Friend VALUES (%s, %s,0,NOW())"
     update_friend_request_list = [request.session['username'],target_username]
     sf_db.execute_sql(friend_request_setence, update_friend_request_list)
     messages.success(request, 'Your request has sent.')
     return HttpResponseRedirect('/friend-confirm')

   if request.POST:
     #add friend to circle
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     circle_info_sentence = """SELECT cid FROM Circle Where cname = %s"""
     #username = target_username
     circle_info_list = sf_db.query_data(circle_info_sentence, request.POST.get('circle'))

     circleid = circle_info_list[0][0]

     print "AA"
     print circleid
     
     add_friend_to_circle_sentence = "INSERT INTO CirclePeople VALUES (%s, %s, 0) "
     update_circlepeople_list = [circleid, target_username]
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     sf_db.execute_sql(add_friend_to_circle_sentence, update_circlepeople_list)
     messages.success(request, 'Friend has been added to circle')
     show_info = {}
     show_info['is_login'] = 'true'
     print request.POST.get('circle')

     return render_to_response('thankyou.html', show_info, context_instance = RequestContext(request)) 
    
   if target_username == request.session['username']:
     return HttpResponseRedirect('/profile')
   #return HttpResponseRedirect('/friend_profile/'+target_username)
   get_already_friend_info_sentence = "SELECT uid2 FROM Friend WHERE uid1 = %s and request = 1"
   get_pending_friend_info_sentence = "SELECT uid2 FROM Friend WHERE uid1 = %s and request = 0"

   print(target_username) 
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   user_info_sentence = """SELECT * FROM User_Info Where uid = %s"""
   username = target_username
   uesr_info_list = sf_db.query_data(user_info_sentence, username)

   already_friend_list = str(sf_db.query_data(get_already_friend_info_sentence, request.session['username']))
   pending_friend_list = str(sf_db.query_data(get_pending_friend_info_sentence, request.session['username']))

   get_location_info_sentence = "SELECT L.name FROM Location as L, User_Info as U WHERE U.lid = L.lid and U.uid = %s "
   profile_map_location_name = sf_db.query_data(get_location_info_sentence,request.session['username'])
 

   print already_friend_list
   print pending_friend_list

   get_all_post_text_sentence = """SELECT distinct P.uid, P.text, u.uname, u.URL,P.lid FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and P.uid = %s and (P.type=0) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'friends') or (P.Visible='private'and P.uid = %s)or(P.uid = %s)) ORDER BY P.date desc"""
   get_all_post_photoandcap_sentence = """SELECT distinct  P.uid, P.URL,P.caption, u.uname, u.URL,P.lid FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and P.uid = %s and (P.type=1) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'public') or (P.Visible='private'and P.uid = %s) or(P.uid = %s)) ORDER BY P.date desc"""
   
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   
   update_all_text_list = [username,request.session['username'],request.session['username'],request.session['username']]
   all_post_text_info = sf_db.query_data(get_all_post_text_sentence,update_all_text_list)
   all_post_photoandcap_info = sf_db.query_data(get_all_post_photoandcap_sentence,update_all_text_list)
    
   show_info = {}
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   show_info['username'] = uesr_info_list[0][0]
   show_info['id'] = uesr_info_list[0][1]
   show_info['description'] = uesr_info_list[0][3]
   show_info['url'] = uesr_info_list[0][5]
   show_info['location'] = profile_map_location_name
   show_info['textinfo'] = all_post_text_info
   show_info['photoinfo'] = all_post_photoandcap_info  

   if target_username in already_friend_list:
      show_info['add_friend_button']= "friend"
   elif target_username in pending_friend_list:
      show_info['add_friend_button']= "pending request"
   else:
      show_info['add_friend_button']= "add friend"

   
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   get_circle_list_sentence = """SELECT a.cname FROM CirclePeople as c, Circle as a Where c.cid = a.cid and c.uid = %s and c.IsOwner = 1"""
   update_circle_list = request.session['username']
   own_circle = sf_db.query_data(get_circle_list_sentence, update_circle_list)
   show_info['list_circle'] =  own_circle
   print("aa:%s", update_circle_list)
   print show_info['list_circle']

   return render_to_response('friend_profile.html', show_info, context_instance = RequestContext(request))
  
def friend_confirm(request):
    
   show_info = {}
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   return render_to_response('friend_confirm.html', show_info, context_instance = RequestContext(request))
  
  
def create_account(request):
   form = DocumentForm()

   if request.POST:
     print("AA") 
     accountname = request.POST.get('username')
     accountid = request.POST.get('userid')
     accountpwd = request.POST.get('pw_input')
     accountpwdcf = request.POST.get('confirmpw_input')
     accountdesc = request.POST.get('description')
     accountlocation = request.POST.get('location')
     filepath = ""
     form = DocumentForm(request.POST, request.FILES)
     print form 

     if form.is_valid():
      print("BB") 
      handle_uploaded_Pfile(request.FILES['docfile'], accountname)
      print(request.FILES['docfile'].name)
        
      path = "http://127.0.0.1:8000/media/user/%s/" % (accountname)
      filepath = path + request.FILES['docfile'].name

     insert_uinfo_list = [accountname,accountid,accountpwd,accountdesc,accountlocation,filepath]
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     user_insert_sentence = """INSERT INTO User_Info VALUES (%s, %s, %s, %s, %s, %s)"""
     if accountpwd != accountpwdcf:
       messages.success(request, 'password not the same')
       return HttpResponseRedirect('/account-confirm')

     sf_db.execute_sql(user_insert_sentence, insert_uinfo_list)
     messages.success(request, 'Thank you.')
     return HttpResponseRedirect('/account-confirm')   

   show_info = {'form': form}
      #show_info['show_info'] = ''
   show_info['is_login'] = 'false'
   return render_to_response('create_account.html', show_info, context_instance = RequestContext(request))

def account_confirm(request):

   show_info = {}
      #show_info['show_info'] = ''
   show_info['is_login'] = 'false'
   return render_to_response('account_confirm.html', show_info, context_instance = RequestContext(request)) 

def friend(request):
    show_info = {}
    sf_db = spoontifylib.SFDBManager.SFDBManager()
    friend_list_sentence = """SELECT distinct f.uid2, u.URL FROM Friend as f, User_Info as u Where u.uid = f.uid2 and f.uid1 = %s and f.request = 1"""
    find_pending_request_sentence = "SELECT uid1 FROM Friend WHERE uid2 = %s and request=0"
  
    username = request.session['username']
    get_friend_list = sf_db.query_data(friend_list_sentence, username)
    print get_friend_list

    circle_list_sentence = """SELECT a.cname, a.cid FROM CirclePeople as c, Circle as a Where c.cid = a.cid and c.uid = %s and c.IsOwner = 1"""
    username = request.session['username']
    get_circle_list = sf_db.query_data(circle_list_sentence, username)
    print("aa:%s", get_circle_list)
  
    
    pending_friend_list = sf_db.query_data(find_pending_request_sentence, username)
    show_info['pending_list'] = pending_friend_list

    


    
      #show_info['show_info'] = ''
    show_info['is_login'] = 'true'
    show_info['friend_list'] = get_friend_list
    show_info['circle_list'] = get_circle_list

    return render_to_response('friend.html', show_info, context_instance = RequestContext(request))   

def friend_request(request, target_username=''):  

    show_info = {}
    sf_db = spoontifylib.SFDBManager.SFDBManager()
    reply_request_sentence = "UPDATE Friend SET request=1 Where uid1=%s and uid2 = %s "
    reply_request_new_sentence = "INSERT INTO Friend VALUES(%s,%s,1,NOW())"
    reply_request_sentence_lsit = [target_username,request.session['username']]
    reply_request_new_sentence_list = [request.session['username'],target_username]
    sf_db.execute_sql(reply_request_sentence, reply_request_sentence_lsit)
    sf_db.execute_sql(reply_request_new_sentence, reply_request_new_sentence_list)
    messages.success(request, 'Already respose friend request')
    return HttpResponseRedirect('/friend')     

def create_circle(request):
   print("AA") 
   if request.POST:
     circlename = request.POST.get('newcircle_input')
     circleid = os.urandom(16)
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     circle_insert_sentence = """INSERT INTO Circle VALUES (%s, %s)"""
     #username = request.session['username']
     insert_rl_set = [circleid, circlename]
     sf_db.execute_sql(circle_insert_sentence, insert_rl_set)

     circle_insert_sentence = """INSERT INTO CirclePeople VALUES (%s, %s, 1)"""
     #username = request.session['username']
     insert_rl_set = [circleid, request.session['username']]
     sf_db.execute_sql(circle_insert_sentence, insert_rl_set)

     show_info = {}
     messages.success(request, 'Circle has been created')
     show_info['is_login'] = 'true'
     return render_to_response('thankyou.html', show_info, context_instance = RequestContext(request)) 
    
   show_info = {}
   show_info['is_login'] = 'true'
   return render_to_response('create_circle.html', show_info, context_instance = RequestContext(request))  

def add_circle(request):
   print("AA") 
   if request.POST:
     show_info = {}
     #add friend to circle
     add_friend_to_circle_sentence = "INSERT INTO CirclePeople VALUES (%s, %s, 0) "
     update_circlepeople_list = [request.POST.get('circle'), ]
     show_info = {}
     sf_db = spoontifylib.SFDBManager.SFDBManager()
     sf_db.execute_sql(add_friend_to_circle_sentence, update_circlepeople_list)
     messages.success(request, 'Friend has been added to circle')
     show_info['is_login'] = 'true'
     print request.POST.get('circle')

     return render_to_response('thankyou.html', show_info, context_instance = RequestContext(request)) 
    
   show_info = {}
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   get_circle_list_sentence = """SELECT cid FROM CirclePeople WHERE uid = %s """
   update_circle_list = request.session['username']
   own_circle = sf_db.query_data(get_circle_list_sentence, update_circle_list)
   show_info['list_circle'] =  own_circle
   print show_info['list_circle']
   print "AAA"
   
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   return render_to_response('friend_profile.html', show_info, context_instance = RequestContext(request))  

def search(request, target_username=''):

   show_info = {}
   print target_username 
     
   get_all_post_text_sentence = """SELECT distinct P.uid, P.text, u.uname, u.URL FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and P.text LIKE %s and (P.type=0) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'friends') or (P.Visible='private'and P.uid = %s)or(P.uid = %s)) ORDER BY P.date desc"""
   get_all_post_photoandcap_sentence = """SELECT distinct  P.uid, P.URL,P.caption, u.uname, u.URL FROM Post as P, Friend as F, User_Info as u WHERE u.uid = P.uid and P.caption LIKE %s and (P.type=1) and( (P.Visible = 'public') or (F.uid1 = %s and F.uid2 =P.uid and P.type=0 and P.Visible= 'public') or (P.Visible='private'and P.uid = %s) or(P.uid = %s)) ORDER BY P.date desc"""
   
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   searchText = "%"+target_username+"%"
   update_all_text_list = [searchText,request.session['username'],request.session['username'],request.session['username']]
   all_post_text_info = sf_db.query_data(get_all_post_text_sentence,update_all_text_list)
   all_post_photoandcap_info = sf_db.query_data(get_all_post_photoandcap_sentence,update_all_text_list)

   people_list_sentence = """SELECT distinct u.uname, u.URL FROM User_Info as u Where u.uname LIKE %s """
   #find_pending_request_sentence = "SELECT uid1 FROM Friend WHERE uid2 = %s and request=0"
   username = request.session['username']
   searchText = "%"+target_username+"%"
   update_all_text_list = [searchText, username]
   get_people_list = sf_db.query_data(people_list_sentence, searchText)

   show_info['textinfo'] = all_post_text_info
   show_info['photoinfo'] = all_post_photoandcap_info
   show_info['people_list'] = get_people_list
    
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   return render_to_response('search.html', show_info, context_instance = RequestContext(request))   

   #return render_to_response('search.html', show_info, context_instance = RequestContext(request))   
def circle_profile(request, target_username=''):

   show_info = {}
   print target_username  
   sf_db = spoontifylib.SFDBManager.SFDBManager()
   people_list_sentence = """SELECT distinct u.uname, u.URL, u.uid FROM User_Info as u, CirclePeople as c Where c.uid = u.uid and c.cid = %s"""
   #find_pending_request_sentence = "SELECT uid1 FROM Friend WHERE uid2 = %s and request=0"

   get_people_list = sf_db.query_data(people_list_sentence, target_username)
   print get_people_list
   #show_info['textinfo'] = all_post_text_info
   #show_info['photoinfo'] = all_post_photoandcap_info
   show_info['people_list'] = get_people_list
    
      #show_info['show_info'] = ''
   show_info['is_login'] = 'true'
   return render_to_response('circle_profile.html', show_info, context_instance = RequestContext(request))   

   #return render_to_response('search.html', show_info, context_instance = RequestContext(request))      


