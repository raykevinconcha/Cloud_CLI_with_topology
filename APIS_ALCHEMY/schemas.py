from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    password: str
    role: int



class User(UserBase):
    idUser: int

    class Config:
        from_attributes = True




class LogBase(BaseModel):
    doc: Optional[bytes]


class Log(LogBase):
    idLogs: int
    doc: Optional[bytes]
    idUsers: int

    class Config:
        from_attributes = True



class SliceBase(BaseModel):
    name: str
    status: int
    number_nodes: str
    number_links: str


class Slice(SliceBase):
    idSlices: int
    idUsers: int

    class Config:
        from_attributes = True




class TokenBase(BaseModel):
    TokenValue: str
    timestamp: datetime



class Token(TokenBase):
    idToken: int
    idSlices: int  

    class Config:
        from_attributes = True


class NodeBase(BaseModel):
    VM_name:str
    capacity: str
    port: str
    description: str
    status: int




class Node(NodeBase):
    MAC: str
    idSlices: int
    idImages: int
    idServers: int
    idflavor: int

    class Config:
        from_attributes = True

class FlavorBase(BaseModel):
    memory: str
    RAM: str
    disk: str


class Flavor(FlavorBase):
    idFlavor: int

    class Config:
        from_attributes = True


class EdgesBase(BaseModel):
    title: str
    


class Edges(EdgesBase):
    idedges: int
    nodes_MAC:str

    class Config:
        from_attributes = True

class SubnetBase(BaseModel):
    name: str
    



class  Subnet(SubnetBase):
    idsubnet: int
    edges_idedges:int

    class Config:
        from_attributes = True

class PortBase(BaseModel):
    name: str
    


class  Port(PortBase):
    idport: int
    idSubnet:int

    class Config:
        from_attributes = True


class ImagesBase(BaseModel):
    name: str
    plataforma:int
    ruta: str
    
    



class  Images(ImagesBase):
    idimages: int
   

    class Config:
        from_attributes = True


class ServersBase(BaseModel):
    ServerName:  str
    ServerIP: str
    ServerStatus: str
    AZ: int
    
    



class  Servers(ServersBase):
    idServers: int
   

    class Config:
        from_attributes = True

class ServerusageBase(BaseModel):
    ServerName: str
    ServerIP: str
    ServerStatus: str
    AZ: int
    


class  Serversusage(ServerusageBase):
    idserverusage: int
    idServers: int
   

    class Config:
        from_attributes = True


class SystemsresourcesBase(BaseModel):
    CPUUsage: str
    memory: str
    disk: str
    timestamp: str
    
    



class  Systemsresources(SystemsresourcesBase):
    idsystemsResources: int
    MAC: str
   

    class Config:
        from_attributes = True