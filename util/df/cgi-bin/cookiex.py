#!/usr/bin/python3
from os import environ
import cgi
#from http import cookies

# cookie variables and initial values
ckvar_id = "studentid"
ckvar_name="name"
ckvar_dept="dept"
ckvar_course="course"

ckval_id = ''
ckval_name = ''
ckval_dept = ''
ckval_course = ''

#create cookie object to explore working with cookie header via cookie object
#cookie = cookies.SimpleCookie()
#In this sample we work only with CGI Environment variables directly.
cookie_str = environ.get('HTTP_COOKIE')

if cookie_str is not None and cookie_str != "":
  cookie_arr = cookie_str.split(";")
  for ck_item in cookie_arr:
    ck_item = ck_item.strip()
    (ck_key, ck_val) = ck_item.split("=")
    if ck_key == ckvar_id:
       ckval_id = ck_val
    if ck_key == ckvar_name:
       ckval_name = ck_val
    if ck_key == ckvar_dept:
       ckval_dept = ck_val
    if ck_key == ckvar_course:
       ckval_course = ck_val
# processing of retrieved cookies over

# set existing cookies
#cookie.load(cookie_str)


print("Content-type: text/html")
print("Host: myweb.local")


form = cgi.FieldStorage()
if ckvar_id in form:
  studentid = form[ckvar_id].value
  print("Set-Cookie:{0} = {1}; Max-Age=3600".format(ckvar_id, studentid))
if ckvar_name in form:
  name = form[ckvar_name].value
  print("Set-Cookie:{0} = {1}".format(ckvar_name, name))
if ckvar_dept in form:
  dept = form[ckvar_dept].value
  print("Set-Cookie:{0} = {1}".format(ckvar_dept, dept))
if ckvar_course in form:
  course = form[ckvar_course].value
  print("Set-Cookie:{0} = {1}".format(ckvar_course, course))

# separating line of headers from web content
print()

print("<htm><body>")
print("<h1>Web page to set cookies</h1>")
print("This web page provides a simple example of setting cookies")
print("<br>The web page does not check if cookies are already set")
print("<h2>Web Form to study Cookies</h2>")

print('<form action = "/cgi-bin/cookiex.py" method = "POST" target = "_blank">')

print(ckvar_id)
print('<br><input type = "text" name = "{0}" value = "{1}" /><br>'.format(ckvar_id, ckval_id))
print(ckvar_name)
print('<br><input type = "text" name = "{0}" value = "{1}" /><br>'.format(ckvar_name, ckval_name))
print(ckvar_dept)
print('<br><input type = "text" name = "{0}" value = "{1}" /><br>'.format(ckvar_dept, ckval_dept))
print(ckvar_course)
print('<br><input type = "text" name = "{0}" value = "{1}" /><br>'.format(ckvar_course, ckval_course))

print('<br><input type = "submit" value = "Submit" />')
print('</form>')


print("</body></html>")




