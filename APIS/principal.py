from fastapi import FastAPI, HTTPException
from fastapi import Depends, HTTPException, status
from database import Database 
from crud import create_slices, get_slices, update_slices, delete_slices, create_logs, get_systemsresources, get_nodes, create_vm_images, create_token
from typing import List
from models import SliceCreate, Slice, LogBase, Systemsresources, Node, Images, Token, Log,LogCreate,ImagesCreate,TokenCreate

app = FastAPI()

def get_db():
    aa = Database()
    try:
        yield aa
    finally:
        aa.close()

@app.post("/slices/", response_model=Slice)
async def create_slices_route(slices: SliceCreate  , db: Database = Depends(get_db)):
    return create_slices(db, slices)

@app.get("/slice/list", response_model=List[Slice])
async def list_slices(db: Database = Depends(get_db)):
    return get_slices(db)

@app.put("/slices/{slices_id}", response_model=Slice)
async def edit_slices(slices_id: int, slices: SliceCreate, db: Database = Depends(get_db)):
    existing_slices = get_slices(db)
    if not existing_slices:
        raise HTTPException(status_code=404, detail="Slices not found")
    return update_slices(db, slices_id, slices)

@app.delete("/slices/{slices_id}", response_model=int)
async def delete_slices_route(slices_id: int, db: Database = Depends(get_db)):
    existing_slices = get_slices(db)
    if not existing_slices:
        raise HTTPException(status_code=404, detail="Slices not found")
    return delete_slices(db, slices_id)

# Rutas CRUD para Logs
@app.post("/logs/", response_model=Log)
async def create_logs_route(logs: LogCreate, db: Database = Depends(get_db)):
    return create_logs(db, logs)

# Rutas para obtener informaciÃ³n
@app.get("/systemsresources/list", response_model=List[Systemsresources])
async def list_systemsresources(db: Database = Depends(get_db)):
    return get_systemsresources(db)

@app.get("/nodes/list", response_model=List[Node])
async def list_nodes(db: Database = Depends(get_db)):
    return get_nodes(db)

# Rutas CRUD para VMImages y Token (creaciÃ³n)
@app.post("/vm_images/", response_model=Images)
async def create_vm_images_route(vm_images: ImagesCreate, db: Database = Depends(get_db)):
    return create_vm_images(db, vm_images)

@app.post("/token/", response_model=Token)
async def create_token_route(token: TokenCreate, db: Database = Depends(get_db)):
    return create_token(db, token)
