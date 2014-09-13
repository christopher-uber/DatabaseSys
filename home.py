__author__ = 'ChrisUber-636652'

import session
import MySQLdb
import sys
import cgi


def NextURL():
    try:
        rows.next()
        return rows['URL']
    except Exception as e:
        return e


def NextName():
    try:
        return rows['Name']
    except Exception as e:
        return e



db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "cuber", "", "cuber", 3306)
cursor = db.cursor(MySQLdb.cursors.DictCursor)

foundParameters = 0
UrlParameters = cgi.FieldStorage()
if UrlParameters.has_key('KeyName'):
    foundParameters = 1

SessionData = session.Session(expires=20*60, cookie_path='/')

print "Content-Type: text/html \n"

print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>WWAG</title>
<meta author="Chris UBER" />
</head>
"""

print """
<body>
<table width="90%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td colspan="2" align="center"><p>&nbsp;</p>
    <p>&nbsp;</p>
    <h1 id="PageTitle">Will Wheaton Appreciation Group</h1>"""

LoggedIn = SessionData.data.get('LoggedIn')
if LoggedIn:
    UserName = session.data['UserName']
    print " <p>Welcome {0}, <a href=\"do_logout.py\">Logout</a></p>".format(UserName)
else:
    print "<p><a href=\"login.py\">Login</a></p>"
print """
  </td>
  </tr>
  <tr>
    <td width="28%" id="Menuitems"><p><a href="#">Home Page</a></p>
    <p><a href="#">Viewers</a></p>
    <p><a href="#">Login</a></p>
    <p><a href="#">Registered Viewers</a></p>
    <p><a href="#">Browse Videos</a></p>
    <p><a href="#">Orders</a></p>
    <p><a href="#">Players</a></p>
    <p><a href="#">Maintance</a></p></td>

"""
try:
    sql = " SELECT URL, Name  FROM Video NATURAL JOIN InstanceRun WHERE VideoType IS NULL ORDER BY uuid() LIMIT 5 "

    cursor.execute(sql)
    rows = iter(cursor.fetchall())

    print """
    <td width="72%" align="center"><p><a name="top" id="top"></a></p>
      <h2>Welcome!</h2>
      <p>Welcome to the Will Wheaton Appreciation Group! Check out some of our videos below for a random sample of what we produce. To log in or to access your premium content, change your information or update a new video, please use the links to the side.</p>
      <p>&nbsp;</p>
      <p>Happy Gaming!</p>
      <table width="90%" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td align="center">
          <video width="320" height="240" controls>
          <source src="{0}" type="video/mp4">
          Your browser does not support the video tag.
          </video>&nbsp;</td>
          <td align="center">
          <video width="320" height="240" controls>
          <source src="{2}" type="video/mp4">
          Your browser does not support the video tag.
          </video>&nbsp;</td>
        </tr>
        <tr>
          <td align="center">{1}</td>
          <td align="center">{3}</td>
        </tr>
        <tr>
          <td align="center">
          <video width="320" height="240" controls>
          <source src="{4}" type="video/mp4">
          Your browser does not support the video tag.
          </video>&nbsp;</td>
          <td align="center">
          <td align="center">
          <video width="320" height="240" controls>
          <source src="{6}" type="video/mp4">
          Your browser does not support the video tag.
          </video>&nbsp;</td>
        </tr>
        <tr>
          <td align="center">{5}</td>
          <td align="center">{7}</td>
        </tr>
      </table>
      <p>&nbsp;</p>
<p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p></td>
  </tr>
    """.format(NextURL(),NextName(),NextURL(),NextName(),NextURL(),NextName(),NextURL(),NextName())
except Exception as e:
    print """
        <td width="72%" align="center"><p><a name="top" id="top"></a></p>
        <h2>Welcome!</h2>
        <p> Error: {0} </p>
        </td>
        </tr> """.format(e)
finally:
    print """
        </table>
        </body>
        </html> """
    cursor.close()
    db.commit()
    db.close()
    SessionData.close()
