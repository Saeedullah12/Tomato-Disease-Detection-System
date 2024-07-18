import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["detectionsystem"]


def get_image_result(name, k_):
  col = db['image_res']
  return col.find_one({'key': k_}, {'_id': 0, 'name': 1, 'confidence': 1})
 
def save_image_result(name, key, conf):
  col = db['image_res']
  return col.insert_one({'name': name, 'key': key, 'confidence': conf, 'createdAt': datetime.now().isoformat()})

  

def _signUp(user):
  createdAt = datetime.now().isoformat()
  col = db['users']
  if col.find_one({'email': user['email']}):
    return {'message': 'Error email already exist!', 'success': 0}
  k = col.insert_one({**user, 'createdAt': createdAt})
  return {'message': 'Successfully login!', 'success': 1} 
    
  

def _login(email, password):
  col = db['users']
  user = col.find_one({'$and': [{"email": email, "password": password}]})
  return user