import jwt
from src.core.config import settings
from datetime import datetime, timedelta

JWT_SECRET = settings.JWT_SECRET
ALGORITHM = "HS256"

def create_jwt_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt



def decode_jwt_token(token:str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except jwt.PyJWTError:
        return None

def decode_google_token(token:str):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except jwt.PyJWTError:
        return None
    
    
print(decode_google_token("eyJhbGciOiJSUzI1NiIsImtpZCI6IjEzMGZkY2VmY2M4ZWQ3YmU2YmVkZmE2ZmM4Nzk3MjIwNDBjOTJiMzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5MTk2NDM2MTg2MzctZWF2Y3M0bnZmMG51N2QzOW5nb25sOXVvcDJycHU1Nm8uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5MTk2NDM2MTg2MzctZWF2Y3M0bnZmMG51N2QzOW5nb25sOXVvcDJycHU1Nm8uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTA2MzA0MzcwMzE4MDUxMDE5OTQiLCJlbWFpbCI6ImJpa2FscGFwYXVkZWw1M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImJEeTkwMFA5Rll3WDVTNTdua0R1UmciLCJuYW1lIjoiQmlrYWxwYSBQYXVkZWwiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTHdFUnJJOEt1LXpZYU1aM0dHZzhnMGdZQkR4c0J6R3BWdEFBU1p3Ukt1bkxrU3FaRlU9czk2LWMiLCJnaXZlbl9uYW1lIjoiQmlrYWxwYSIsImZhbWlseV9uYW1lIjoiUGF1ZGVsIiwiaWF0IjoxNzY1NjAxMzg5LCJleHAiOjE3NjU2MDQ5ODl9.L_RxA7XzzvReZlhalK97kOXSMoa8OQirm131ELFkKBQcc59TOL9Yoq8WVAvw93cpwBNfLstfrnqbS-AmofF3eJ3ijlxe4kOOK9HLnun3roWeZxNOeMg6GaPNB4tbnRpClNaZBpXYR4MCvb1x-hFOLvA2NUGOtesK_DZq5Q2MSNpcKK0aLo5NCrUNNRpRlJfOHatojaERfllGOxuI2VUs6aQVPumL9wRtpF0B6blto6kRx9GCPYFmAjGFu5rjAcX_X21AbRKAN5PFxrOumIZf1T4DEtLagRTYbJUGsFXj-4McJQwFPSOwAibDMjX4iz1FsNDnjup9x1lmLL8zB31wiA"))
