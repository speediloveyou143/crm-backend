# config.py
from mongoengine import connect

def init_db():
    try:
        connect(
            db='jhc-crm',
            host='mongodb://localhost:27017/crm',
            alias='default'
        )
        print("✅db connection success")
    except:
        print("❌db connection failed")
        
        