
from database import Database
from models import SliceCreate, Slice, LogCreate, Log, Systemsresources, NodeCreate, Node, ImagesCreate, ImagesBase, TokenCreate, Token

def create_slices(db: Database, slices: SliceCreate):
    query = "INSERT INTO Slices (name, status, number_nodes, number_links, Users_idUsers, Topology_idTopology) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (slices.name, slices.status, slices.number_nodes, slices.number_links, slices.Users_idUsers, slices.Topology_idTopology)
    return db.execute_insert_query(query, data)

def get_slices(db: Database):
    query = "SELECT * FROM slices"
    return db.execute_query(query)

def update_slices(db: Database, slices_id: int, slices: SliceCreate):
    query = "UPDATE Slices SET name = %s, status = %s, number_nodes = %s, number_links = %s WHERE idSlices = %s"
    data = (slices.name, slices.status, slices.number_nodes, slices.number_links, slices_id)
    db.execute_query(query, data)

def delete_slices(db: Database, slices_id: int):
    query = "DELETE FROM Slices WHERE idSlices = %s"
    data = (slices_id,)
    db.execute_query(query, data)

def create_logs(db: Database, logs: LogCreate):
    query = "INSERT INTO Logs (log_activityType, log_Timestamp, Users_idUsers) VALUES (%s, %s, %s)"
    data = (logs.log_activityType, logs.log_Timestamp, logs.Users_idUsers)
    return db.execute_insert_query(query, data)

def get_systemsresources(db: Database):
    query = "SELECT * FROM sytemsresources"
    return db.execute_query(query)

def get_nodes(db: Database):
    query = "SELECT * FROM nodes"
    return db.execute_query(query)

def create_vm_images(db: Database, vm_images: ImagesCreate):
    query = "INSERT INTO VMImages (name, Slices_idSlices) VALUES (%s, %s)"
    data = (vm_images.name, vm_images.Slices_idSlices)
    return db.execute_insert_query(query, data)

def create_token(db: Database, token: TokenCreate):
    query = "INSERT INTO Token (Slices_idSlices, TokenValue) VALUES (%s, %s)"
    data = (token.Slices_idSlices, token.TokenValue)
    return db.execute_insert_query(query, data)
