from fastapi import FastAPI ,Response ,status ,HTTPException, Request
from fastapi.params import Body          #FOR POST RESPONSE
from pydantic import BaseModel           #FOR SCHEMA
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
import threading
import requests

from starlette.middleware.cors import CORSMiddleware
import psycopg2                     # for databse connection
from psycopg2.extras import RealDictCursor
import time

app =FastAPI()



#                                       Schema class for post
class login(BaseModel):
    name: str
    type: str      = "test"   #test is default if not filled
    mobile_no: int
    pin: int
    house_no: int
    street: str
    block_no: int
    tehsil: str
    pincode: int


# Declare global variables
conn = None
cursor = None
                    #connection with database

def start():
    global conn, cursor
    while True:
        try:
            conn = psycopg2.connect(host = 'db.vholtltfpdmccdgybxaa.supabase.co', database ='postgres', 
                                user='postgres' ,password ='PragunJaswal',cursor_factory= RealDictCursor)
            cursor = conn.cursor()
            print("DATABASE CONNECTED")
            break

        except Exception as error:
            print("Connection is not Establised")
            print("Error was ",error)
            time.sleep(2)

templates =Jinja2Templates(directory="templates")

start()

@app.get("/")
def root():
    return{"server is running, Made by Pragun Jaswal"}

# Define a function to periodically fetch and print the API response
def print_api_response():
    api_url = "https://swachhdhan.onrender.com/"
    while True:
        try:
            # Make a GET request to the API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the API response content
                print(response.text)
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Wait for 5 seconds before making the next request
        time.sleep(60)


# Create a background thread to run the print_api_response function
background_thread = threading.Thread(target=print_api_response)

# Start the background thread when the application start
@app.on_event("startup")
def on_startup():
    background_thread.start()



@app.get("/get/data/login")
def getpost():
    try:
        cursor.execute("""SELECT * FROM public."Login database" ORDER BY id DESC """)
        login = cursor.fetchall()
        return{ "data":login }
    except Exception :
        start()
        print("DATABASE CONNECTED")
        return {"Error in database connection"}
    

@app.post("/post/data/login",status_code=201)        #DEFAULT RESPONSE 201
def post(payload: login):
    cursor.execute("""INSERT INTO "Login database" (name,type,mobile_no,pin,house_no,street,block_no,tehsil,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",(
    payload.name,payload.type,payload.mobile_no,payload.pin,payload.house_no,payload.street,payload.block_no,payload.tehsil,payload.pincode))
    new =cursor.fetchone()
    conn.commit()
    conn.rollback()
    return {"Success":new }

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
