
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    password: str
    role: int

class UserCreate(UserBase):
    idUser: int

    pass

class User(UserBase):
    idUser: int

    class Config:
        orm_mode = True




class LogBase(BaseModel):
    doc: Optional[bytes]

class LogCreate(LogBase):
    idUsers: int

class Log(LogBase):
    idLogs: int
    doc: Optional[bytes]
    idUsers: int

    class Config:
        orm_mode = True



class SliceBase(BaseModel):
    name: str
    status: int
    number_nodes: str
    number_links: str

class SliceCreate(SliceBase):
    idUsers: int

class Slice(SliceBase):
    idSlices: int
    idUsers: int

    class Config:
        orm_mode = True




class TokenBase(BaseModel):
    TokenValue: str
    timestamp: datetime

class TokenCreate(TokenBase):
    idSlices: int

class Token(TokenBase):
    idToken: int
    idSlices: int  

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    VM_name:str
    capacity: str
    port: str
    description: str
    status: int


class NodeCreate(NodeBase):
    MAC: str
    pass

class Node(NodeBase):
    MAC: str
    idSlices: int
    idImages: int
    idServers: int
    idflavor: int

    class Config:
        orm_mode = True

class FlavorBase(BaseModel):
    memory: str
    RAM: str
    disk: str

class FlavorCreate(FlavorBase):
    idFlavor: int
    pass

class Flavor(FlavorBase):
    idFlavor: int

    class Config:
        orm_mode = True


class EdgesBase(BaseModel):
    title: str
    

class EdgesCreate(EdgesBase):
    idedges: int
    pass

class Edges(EdgesBase):
    idedges: int
    nodes_MAC:str

    class Config:
        orm_mode = True

class SubnetBase(BaseModel):
    name: str
    

class  SubnetCreate(SubnetBase):
    idsubnet: int
    pass

class  Subnet(SubnetBase):
    idsubnet: int
    edges_idedges:int

    class Config:
        orm_mode = True

class PortBase(BaseModel):
    name: str
    

class  PortCreate(PortBase):
    idport: int
    pass

class  Port(PortBase):
    idport: int
    idSubnet:int

    class Config:
        orm_mode = True


class ImagesBase(BaseModel):
    name: str
    plataforma:int
    ruta:str
    
    

class  ImagesCreate(ImagesBase):
    idimages: int
    pass

class  Images(ImagesBase):
    idimages: int
   

    class Config:
        orm_mode = True


class ServersBase(BaseModel):
    ServerName: str
    ServerIP:str
    ServerStatus:str
    AZ:int
    
    

class  ServersCreate(ServersBase):
    idServers: int
    pass

class  Servers(ServersBase):
    idServers: int
   

    class Config:
        orm_mode = True

class ServerusageBase(BaseModel):
    ServerName: str
    ServerIP:str
    ServerStatus:str
    AZ:int
    
    

class  ServerusageCreate(ServerusageBase):
    idserverusage: int
    pass

class  Servers(ServerusageBase):
    idserverusage: int
    idServers:int
   

    class Config:
        orm_mode = True


class SystemsresourcesBase(BaseModel):
    CPUUsage: str
    memory:str
    disk:str
    timestamp:str
    
    

class  SystemsresourcesCreate(SystemsresourcesBase):
    idsystemsResources: int
    pass

class  Systemsresources(SystemsresourcesBase):
    idsystemsResources: int
    MAC:str
   

    class Config:
        orm_mode = True