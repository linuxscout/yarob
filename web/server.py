from fastapi import FastAPI,Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import adaat

app = FastAPI()

# allow all origins, using wildcard, when frontend interface origins are known, remove wildcard.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#mount static files, templates TODO: can we make directoreis simpler ? 
app.mount("/static", StaticFiles(directory="static"), name ="static")
templates = Jinja2Templates(directory ="static/templates")

@app.get('/',include_in_schema=False,response_class=HTMLResponse)
def index(request : Request):
    return  templates.TemplateResponse("index.html", {"request":request})
@app.get("/ajaxGet")
def getAjax(text: str, action: str,order:int=0,lastmark:int=0):
    '''
    TODO: we need typechecking here (for all params, and for the set of actions), we can use pydantic, and BaseModel to achive that
    we have actions,text,option. a better structure would use options as query params
    and text as payload
    and actions as endpoint or payload type
    for now, im settling with the current structure, but there is room to improve.
    '''
    resulttext = adaat.DoAction(text, action,{"order":order,"lastmark":lastmark})
    results = {'result':resulttext, 'order':0}
    return  results
