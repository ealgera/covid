from os     import environ
from dotenv import load_dotenv
load_dotenv() # Laad de ENV variablelen uit het .env bestand

SECRET_KEY    = environ.get("SECRET_KEY")
UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
RECS_PER_PAGE = 15

DE_DATA       = environ.get("DE_DATA")

#EXPLAIN_TEMPLATE_LOADING = True

#UPLOAD_FOLDER = "/static/upload/"

#print(f" --> KEY: {SECRET_KEY}")
