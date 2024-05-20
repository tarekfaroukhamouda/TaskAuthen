import os
from pathlib import Path
from dotenv import load_dotenv

path_env=Path('.')/".env"
load_dotenv(dotenv_path=path_env)
class Settings:
    PROJECT_NAME="Integration"
    PROJECT_VERSION="0.1"
    API_LOGIN_ID=os.getenv("API_LOGIN_ID")
    TRANSACTION_KEY=os.getenv("TRANSACTION_KEY")
    
lol=Settings()