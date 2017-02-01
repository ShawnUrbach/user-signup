#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def build_page(userValue,passValue,verifyValue,emailValue,user_error,pass_error,verify_error,email_error):

    head = '<head><link rel="stylesheet" type="text/css" href="/css/mystyle.css"></head>'

    username_label = "<label>Username: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>"
    username_input = "<input name='username' value='"+userValue+"'/>"
    user_total = username_label+username_input

    password_label = "<label>Password: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>"
    password_input = "<input name='password' type='password' value='"+passValue+"'/>"
    pass_total = password_label+password_input

    verify_label = "<label>Verify Password: </label>"
    verify_input = "<input name='verify' type='password' value='"+verifyValue+"'/>"
    verify_total = verify_label+verify_input

    email_label = "<label>Email: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>"
    email_input = "<input name='email' value='"+emailValue+"'/>"
    email_total = email_label+email_input

    submit = "<input type = 'submit'/>"

    form = ("<form method='post'>" +
        user_total + user_error + "<br>" +
        pass_total + pass_error + "<br>" +
        verify_total + verify_error + "<br>" +
        email_total + email_error + "<br>" +
        submit + "</form>")

    header = "<h2>User Signup</h2>"
    return head + header + form

class MainHandler(webapp2.RequestHandler):

    def get(self):

        content = build_page('','','','','','','','')
        self.response.write(content)

    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        global glob_user
        glob_user = self.request.get("username")

        error = '<span class = "error"> Field entered incorrectly.</span>'
        errorMatch = '<span class = "error"> Passwords must match.</span>'

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PW_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        def valid_username(username):
            return USER_RE.match(username)

        def valid_password(password):
            return PW_RE.match(password)

        def valid_email(email):
            return EMAIL_RE.match(email)

        if valid_username(username) == None:
            if valid_password(password) == None and valid_email(email) == None:
                self.response.write(build_page(username,'','',email,error,error,'',error))

            elif valid_password(password) == None and valid_email(email):
                self.response.write(build_page(username,'','',email,error,error,'',''))

            elif valid_password(password) and valid_email(email) == None:
                self.response.write(build_page(username,'','',email,error,'','',error))

            else:
                self.response.write(build_page(username,'','',email,error,'','',''))

        elif valid_password(password) == None:
            if valid_username(username) == None and valid_email(email):
                self.response.write(build_page(username,'','',email,error,error,'',''))

            elif valid_username(username) and valid_email(email) == None:
                self.response.write(build_page(username,'','',email,'',error,'',error))

            else:
                self.response.write(build_page(username,'','',email,'',error,'',''))

        elif valid_email(email) == None:
            if valid_username(username) == None and valid_password(password):
                self.response.write(build_page(username,'','',email,error,'','',error))

            elif valid_username(username) and valid_password(password) == None:
                self.response.write(build_page(username,'','',email,'',error,'',error))

            else:
                self.response.write(build_page(username,'','',email,'','','',error))

        elif password != verify:
            if valid_username(username) == None and valid_email(email) == None:
                self.response.write(build_page(username,'','',email,error,errorMatch,'',error))
            elif valid_username(username) and valid_email(email) == None:
                self.response.write(build_page(username,'','',email,'',errorMatch,'',error))
            elif valid_username(username) == None and valid_email(email):
                self.response.write(build_page(username,'','',email,error,errorMatch,'',''))
            else:
                self.response.write(build_page(username,'','',email,'',errorMatch,'',''))

        else:
            self.response.write(build_page(username,'','',email,'','','',''))

        if valid_username(username) and valid_password(password) and password == verify and valid_email(email):
            self.redirect("/Welcome")

class Welcome(webapp2.RequestHandler):

    def get(self):

        self.response.write('<h2>Welcome ' + glob_user + '</h2>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', Welcome)
], debug=True)
