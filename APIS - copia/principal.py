from fastapi import FastAPI, HTTPException
from fastapi import Depends, HTTPException, status
from database import Database 
from crud import get_slices, get_systemsresources, get_nodes
from typing import List
from models import Slice, LogBase, Systemsresources, Node, Images, Token, Log

app = FastAPI()

def get_db():
    aa = Database()
    try:
        yield aa
    finally:
        aa.close()



@app.get("/slice/list", response_model=List[Slice])
async def list_slices(db: Database = Depends(get_db)):
    return get_slices(db)


# Rutas para obtener informaciÃ³n
@app.get("/systemsresources/list", response_model=List[Systemsresources])
async def list_systemsresources(db: Database = Depends(get_db)):
    return get_systemsresources(db)

@app.get("/nodes/list", response_model=List[Node])
async def list_nodes(db: Database = Depends(get_db)):
    return get_nodes(db)


