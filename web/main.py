from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import adaat
import json
app = FastAPI()
# we allow all origins, using wildcard, when frontend interface origins are known, remove wildcard.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',include_in_schema=False)
def home():
    return  get_swagger_ui_html(openapi_url=app.openapi_url,title=app.title + " - Swagger UI",)
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
