''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
from fastapi import FastAPI, Request              # The main FastAPI import and Request object
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.templating import Jinja2Templates    # Used for generating HTML from templatized files
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
from fastapi.responses import RedirectResponse    # User for 
import uvicorn                                    # Used for running the app directly through Python
import dbutils as db                              # Import helper module of database functions!
import os
import mysql.connector as mysql
from dotenv import load_dotenv
# import init-db.sql
import datetime

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
app = FastAPI()                                   # Specify the "app" that will run the routing
views = Jinja2Templates(directory='views')        # Specify where the HTML files are located
static_files = StaticFiles(directory='public')    # Specify where the static files are located
app.mount('/public', static_files, name='public') # Mount the static files directory to /public

''' Environment Variables '''
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Home route to load the login page

# GET /
@app.get('/', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  with open("index.html") as html:
      return HTMLResponse(content=html.read())

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# RESTful User Routes

# POST /validate
# User is attempting to log in so validate
@app.post('/validate')
async def post_user(request:Request) -> dict:
  '''
  1. Retrieve the data asynchronously from the 'request' object
  2. Extract the username and password
  3. Access Database data and determine authentication status
    - If not authenticated then refuse login entry
  4. If authenticated then create token for user
  5. Give token to user in the form of session data
  6. Redirect to the route '/table'
  '''
  data = await request.json() # data = {"uname":username, "psw":Password}
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT * FROM members where username='" + username + "' AND pass='" + psw + "';")
  

  return {}

# GET /table
# Home route to load the main page in a templatized fashion
@app.get('/table', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  return views.TemplateResponse('views/table.html', {'request':request, 'users':db.select_users()})

# GET /users
# Used to query a collection of all users
@app.get('/users')
def get_users() -> dict:
  '''
  1. Query the database for all users
  2. Format the results as a list of dictionaries (JSON objects!) where the dictionary keys are:
    'id', 'first_name', and 'last_name'
  3. Return this collection as a JSON object, where the key is 'users' and the value is the list
  '''

  users = db.select_users()
  keys = ['id', 'first_name', 'last_name']
  users = [dict(zip(keys, user)) for user in users]
  return {"users": users}

# GET /users/{user_id}
# Used to query a single user
@app.get('/users/{user_id}')
def get_user(user_id:int) -> dict:
  '''
  1. Query the database for the user with a database ID of 'user_id'
  2. If the user does not exist, return an empty object
  3. Otherwise, format the result as JSON where the keys are: 'id', 'first_name', and 'last_name'
  4. Return this object
  '''

  user = db.select_users(user_id)
  response = {} if user==None else {'id':user[0], 'first_name':user[1], 'last_name':user[2]}
  return response

# POST /users
# Used to create a new user
@app.post("/users")
async def post_user(request:Request) -> dict:
  '''
  1. Retrieve the data asynchronously from the 'request' object
  2. Extract the first and last name from the POST body
  3. Create a new user in the database
  4. Return the user record back to the client as JSON
  '''

  data = await request.json()
  first_name, last_name = data['first_name'], data['last_name']
  new_id = db.create_user(first_name, last_name)

  # Send the new record back
  return get_user(new_id)

# PUT /users/{user_id}
@app.put('/users/{user_id}')
async def put_user(user_id:int, request:Request) -> dict:
  '''
  1. Retrieve the data asynchronously from the 'request' object
  2. Attempt to update the user first and last name in the database
  3. Return the update status under the 'success' key
  '''

  data = await request.json()
  first_name, last_name = data['first_name'], data['last_name']
  return {'success': db.update_user(user_id, first_name, last_name)}

# DELETE /users/{user_id}
@app.delete('/users/{user_id}')
def delete_user(user_id:int) -> dict:
  '''
  1. Attempt to delete the user from the database
  2. Return the delete status under the 'success' key
  '''

  return {'success': db.delete_user(user_id)}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If running the server directly from Python as a module
if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)