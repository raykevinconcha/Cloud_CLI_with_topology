
from database import Database
from models import Slice, Log, Systemsresources, Node, ImagesBase, Token



def get_slices(db: Database):
    query = "SELECT s.name, s.number_nodes, s.number_links FROM mydb.slices as s LEFT JOIN users u ON u.idUsers = s.idUsers LEFT JOIN nodes n ON n.idSlices = s.idSlices;"
    return db.execute_query(query)



def get_systemsresources(db: Database):
    query = "SELECT * FROM sytemsresources"
    return db.execute_query(query)

def get_nodes(db: Database):
    query = "SELECT * FROM nodes"
    return db.execute_query(query)


