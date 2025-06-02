# https://docs.pydantic.dev/latest/

from pydantic import BaseModel

class WorkingExperienceBase(BaseModel):
    we_id: int 
    job_title: str | None = None
    company_name: str | None = None
    job_description: str | None = None
    start_date: str| None = None
    end_date: str | None = None
    image_path: str | None = None

class EducationBase(BaseModel):
    edu_id: int
    school_name: str | None = None
    degree: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    image_path: str | None = None

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    is_active: bool
    
    class Config:
        from_attributes = True
