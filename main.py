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


                    #connection with database
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


@app.get("/")
def root():
    return{"server is running, Made by Pragun Jaswal"}

@app.get("/get/data/login")
def getpost():
    cursor.execute("""SELECT * FROM public."Login database" ORDER BY id DESC """)
    login = cursor.fetchall()
    return{ "data":login }

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
