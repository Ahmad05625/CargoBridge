from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, abort
)
from pymongo import MongoClient, DESCENDING
from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps
import bcrypt
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client    = MongoClient(MONGO_URI)
db        = client["cargobridge"]
users_col        = db["users"]
def seed():
    if users_col.find_one({"username": "admin"}):
        return "<p>Admin already exists. Remove /seed route before deploying.</p>"

    hashed = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
    users_col.insert_one({
        "username":   "admin",
        "password":   hashed,
        "role":       "admin",
        "full_name":  "System Administrator",
        "email":      "admin@cargobridge.pk",
        "created_at": datetime.utcnow(),
    })
    return "<p>Admin created. Username: <b>admin</b> | Password: <b>admin123</b>. Remove this route now.</p>"
seed()
