from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

users = []

class User(BaseModel):
    id: int
    username: str
    age: int
class UserCreate(BaseModel):
    id: int = Field(ge=1, le=100, description='Enter User ID')
    username: str = Field(min_length=3, max_length=20, description='Enter Username')
    age: int = Field(ge=18, le=100, description='Enter User age')

app = FastAPI()

@app.get('/users')
async def get_all_users():
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def create_user(user: UserCreate):
    new_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, user: UserCreate):
    for u in users:
        if u.id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return u
    raise HTTPException(status_code=404, detail='User was not found')