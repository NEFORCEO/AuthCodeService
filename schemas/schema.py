from pydantic import BaseModel

class ParamSchema(BaseModel):
    username: str
    
class GetSchema(BaseModel):
    username: str 
    code: int 