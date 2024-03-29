from typing import List
from fastapi import FastAPI, HTTPException,Body
from password_auth_api import Authenticator
from fetch_config import class_obj
from fastapi.middleware.cors import CORSMiddleware
import password_auth_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(user_detail=Body()):
    credentials, locked_accounts = class_obj.dload_creds()
    if user_detail['username'] == 'admin' and user_detail['password'] == 'admin':
        response = locked_accounts
        return {"message": response,"status":"admin"}
    
    else:
        try:
            stored_username = next(user for user, data in credentials.items() if data["username"] == user_detail['username'])
        except:
            return{"message":"User not found","status":"error"}
        if stored_username:
            if user_detail['username'] in locked_accounts:
                #raise HTTPException(status_code=404, detail="Account is locked") 
                return {"message": "Account is locked","status":"error"}
            response,status = Authenticator.password_auth(stored_username, user_detail['password'])
            return {"message": response,"status": status}

@app.put("/updateLockedAccounts")
async def update_locked_accounts(lockedAccounts=Body()):
    class_obj.uload_creds(lockedAccounts["locked_list"])
    password_auth_api.locked_accounts=lockedAccounts["locked_list"]
    return {"message": "Locked accounts updated successfully"}

#uvicorn fast_api:app --reload