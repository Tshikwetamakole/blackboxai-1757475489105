from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

from models import User, UserInDB, UserCreate, UserLogin, Token, Ad, AdInDB, AdCreate, AdUpdate
from auth import verify_password, get_password_hash, create_access_token, verify_token
from database import users_collection, ads_collection

load_dotenv()

app = FastAPI(title="LimpopoConnect 2.0 API", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Helper functions
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = users_collection.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return UserInDB(**user, id=str(user["_id"]))

# Routes
@app.post("/register", response_model=User)
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict["role"] = "user"
    result = await users_collection.insert_one(user_dict)
    new_user = await users_collection.find_one({"_id": result.inserted_id})
    return User(**new_user, id=str(new_user["_id"]))

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@app.post("/ads", response_model=Ad)
async def create_ad(ad: AdCreate, current_user: UserInDB = Depends(get_current_user)):
    ad_dict = ad.dict()
    ad_dict["user_id"] = current_user.id
    result = await ads_collection.insert_one(ad_dict)
    new_ad = await ads_collection.find_one({"_id": result.inserted_id})
    return Ad(**new_ad, id=str(new_ad["_id"]))

@app.get("/ads", response_model=List[Ad])
async def get_ads(skip: int = 0, limit: int = 10):
    ads = []
    cursor = ads_collection.find().skip(skip).limit(limit)
    async for ad in cursor:
        ads.append(Ad(**ad, id=str(ad["_id"])))
    return ads

@app.get("/ads/{ad_id}", response_model=Ad)
async def get_ad(ad_id: str):
    ad = await ads_collection.find_one({"_id": ObjectId(ad_id)})
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return Ad(**ad, id=str(ad["_id"]))

@app.put("/ads/{ad_id}", response_model=Ad)
async def update_ad(ad_id: str, ad_update: AdUpdate, current_user: UserInDB = Depends(get_current_user)):
    ad = await ads_collection.find_one({"_id": ObjectId(ad_id)})
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    if ad["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = {k: v for k, v in ad_update.dict().items() if v is not None}
    await ads_collection.update_one({"_id": ObjectId(ad_id)}, {"$set": update_data})
    updated_ad = await ads_collection.find_one({"_id": ObjectId(ad_id)})
    return Ad(**updated_ad, id=str(updated_ad["_id"]))

@app.delete("/ads/{ad_id}")
async def delete_ad(ad_id: str, current_user: UserInDB = Depends(get_current_user)):
    ad = await ads_collection.find_one({"_id": ObjectId(ad_id)})
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    if ad["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await ads_collection.delete_one({"_id": ObjectId(ad_id)})
    return {"message": "Ad deleted"}

# Mock email function
def send_email(to: str, subject: str, body: str):
    print(f"Sending email to {to}: {subject} - {body}")

@app.post("/forgot-password")
async def forgot_password(email: str):
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # In real implementation, generate reset token and send email
    send_email(email, "Password Reset", "Reset your password here")
    return {"message": "Password reset email sent"}
