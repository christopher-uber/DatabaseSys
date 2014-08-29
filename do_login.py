# The libraries we'll need
import sys, cgi, session, redirect, MySQLdb

# ---------------------------------------------------------------------------------------------------------------------
sess = session.Session(expires=20*60, cookie_path='/')
loggedIn = sess.data.get('loggedIn')

# ---------------------------------------------------------------------------------------------------------------------
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

# ---------------------------------------------------------------------------------------------------------------------
# login logic
if loggedIn:
    
    # redirect to home page
    print """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url=%s">
    </head>
    <body>
    </body>
    """ % redirect.getQualifiedURL(""/~seanbm/Junk/W9LectFiles/home.py"")
    
else:
    form = cgi.FieldStorage()
    if not (form.has_key('username') and form.has_key('password')):
        sess.data['loggedIn'] = 0
    else:
        # Check user's username and password
        db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003", "cisds", "info20003", 3306)
        #get check if we get a row from the database for this user and password
        #cursor = db.cursor()
        #cursor.execute ("""
        #    SELECT user_name
        #    FROM bb_reg_user
        #    WHERE user_name = %s
        #      AND user_password = %s
        #""", (form["username"].value, form["password"].value))
        #if cursor.rowcount == 1:
        #    sess.data['loggedIn'] = 1
        #    row = cursor.fetchone()
        #    sess.data['userName'] = row[0]
        
        #REMOVE THESE LINES FOR REAL IMPLEMENTATION
        sess.data['loggedIn'] = 1
        sess.data['userName'] = form["username"].value
        
        #else:
        #    sess.data['loggedIn'] = 0

        
        
        # tidy up
        #cursor.close()
        db.close()

    whereToNext = "/~seanbm/Junk/W9LectFiles/home.py" if sess.data['loggedIn'] == 1 else "/~seanbm/Junk/W9LectFiles/login.py"
    sess.close()
    
    # redirect to home page or back to the login page
    print """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url=%s">
    </head>
    <body>
    </body>
    """ % redirect.getQualifiedURL(whereToNext)

