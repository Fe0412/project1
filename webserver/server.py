#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://jy2736:WHNJZX@w4111db.eastus.cloudapp.azure.com/jy2736"
#DATABASEURI = "sqlite:///test.db"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#

'''
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
'''
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  '''
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)
  '''


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")#, **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#

@app.route('/users')
def users():
  cursor = g.conn.execute("SELECT name FROM users")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("users.html", **context)

@app.route('/express_company')
def express_company():
  cursor = g.conn.execute("SELECT e_name,e_address FROM express_company")
  names = []
  for result in cursor:
    names.append("name: " + result['e_name'] + ", " + "address: " + result['e_address'])
  cursor.close()
  context = dict(data = names)
  return render_template("express_company.html", **context)

'''
@app.route('/orderInColumbus')
def orderInColumbus():
  #orderin = request.form['address']
  cursor = g.conn.execute("SELECT * FROM Orders WHERE address = 'Apt1 968 Columbus NY10026' ")
  ColumbusOrders = []
  for result in cursor:
    ColumbusOrders.append(result['order_number'])# can also be accessed using result[0]
    ColumbusOrders.append(result['address'])
    ColumbusOrders.append(result['uid'])
    ColumbusOrders.append(result['o_time'])
  cursor.close()
  context = dict(data = ColumbusOrders)

  return render_template("orderInColumbus.html", **context)
'''

@app.route('/orderSum')
def orderSum():
  return render_template("orderSum.html")#, **context)

@app.route('/returnn')
def returnn():
  return render_template("returnn.html")

@app.route('/product')
def product():
  return render_template("product.html")

@app.route('/rate')
def rate():
  cursor =  g.conn.execute("SELECT *FROM rate")
  ratee = []
  for result in cursor:
    ratee.append("uid: " + str(result['uid']) + ", p_name:" + result['p_name'] + ", star: " + str(result['star']))
  cursor.close()
  context = dict(data = ratee)
  return render_template("rate.html", **context)

@app.route('/review')
def review():
  return render_template("review.html")

@app.route('/sell')
def sell():
  cursor = g.conn.execute("SELECT u.uid,u.name FROM customer cu, sell s, users u WHERE cu.uid = s.uid AND u.uid = s.uid")
  sellers = []
  for result in cursor:
    sellers.append("uid: " + str(result['uid']) + ", " + "name: " + result['name'])
  cursor.close()
  context = dict(data = sellers)
  return render_template("sell.html", **context)


'''
Functions
'''

# Example of adding new data to the database
@app.route('/addusers', methods=['GET', 'POST'])
def addusers():
  uid = request.form['uid']
  since = request.form['since']
  email = request.form['email']
  name = request.form['name']
  res = (uid, since, email, name)
  g.conn.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', res)
  return redirect('/users')

@app.route('/deleteusers', methods=['GET', 'POST'])
def deleteusers():
  uid = request.form['uid']
  g.conn.execute('DELETE FROM users WHERE uid = %s', uid)
  return redirect('/users')

@app.route('/ordertotal', methods=['GET', 'POST'])
def ordertotal():
  order_number = request.form['order_number']
  cursor = g.conn.execute('SELECT SUM (price*number) FROM Sell WHERE order_number = %s ', order_number)
  ordersm = []
  for result in cursor:
    ordersm.append(result[0])
  cursor.close()
  context = dict(data = ordersm)
  return render_template("orderSum.html", **context)

@app.route('/addecompany', methods=['GET', 'POST'])
def addecompany():
  name = request.form['e_name']
  address = request.form['e_address']
  res = (name, address)
  g.conn.execute('INSERT INTO express_company VALUES (%s, %s)', res)
  return redirect('/express_company')

@app.route('/returninfo', methods=['GET', 'POST'])
def returninfo():
  order_number = request.form['order_number']
  cursor =  g.conn.execute("SELECT * FROM return WHERE order_number = %s ", order_number)
  ordersm = []
  for result in cursor:
    ordersm.append("suid: " + str(result['suid']) + ", " + "name: " +result['p_name'])
  cursor.close()
  context = dict(data = ordersm)
  return render_template("returnn.html", **context)

@app.route('/proinfo', methods=['GET', 'POST'])
def proinfo():
  p_name = request.form['p_name']
  cursor =  g.conn.execute("SELECT description FROM product WHERE p_name = %s ", p_name)
  des = []
  for result in cursor:
    des.append(result['description'])
  cursor.close()
  context = dict(data = des)
  return render_template("product.html", **context)


@app.route('/rateinfo', methods=['GET', 'POST'])
def rateinfo():
  uid = request.form['uid']
  p_name = request.form['p_name']
  star = request.form['star']
  g.conn.execute("UPDATE rate SET star = %s WHERE uid = %s AND p_name = %s ", star, uid, p_name)
  return redirect('/rate')

@app.route('/reviewinfo', methods=['GET', 'POST'])
def reviewinfo():
  p_name = request.form['p_name']
  cursor =  g.conn.execute("SELECT p_name, uid, content FROM review WHERE p_name= %s ", p_name)
  cont = []
  for result in cursor:
    cont.append("product name: " + result['p_name'] + ", user id: " + str(result['uid']) + ", review: " + result['content'])
  cursor.close()
  context = dict(data = cont)
  return render_template("review.html", **context)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%s" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
