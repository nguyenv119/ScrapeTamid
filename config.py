from dataclasses import dataclass
from typing import Optional
from dotenv import dotenv_values
config = dotenv_values(".env")

@dataclass
class Config:
    start: int
    end: int
    email: str
    password: str
    debug: bool = False
    test: Optional[int] = None 
    delay: float = .5
    base_url: str = 'https://apps.tamidgroup.org/Consulting/Company/posting?id='
    login_url = 'https://apps.tamidgroup.org/login'

email = config["email"]
password = config["password"]
if email == None or password == None:
    raise Exception("Please set EMAIL and PASSWORD in .env file")

config = Config(
    # Edit start and end here, and email / password in .env
    start=9000,
    end=11000,
    email=email,
    password=password,
)