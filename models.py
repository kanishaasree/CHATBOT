from pydantic import BaseModel

class Message(BaseModel):
    role: str  
    content: str
class User(BaseModel):
    email: str
    password: str