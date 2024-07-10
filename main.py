from dotenv import load_dotenv 
from requests import post, get
import os 
import base64
import json

load_dotenv() 

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def main():
    pass 

if __name__ == "__main__":
    main()