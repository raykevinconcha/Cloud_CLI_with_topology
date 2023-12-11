from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, SmallInteger, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    idUser = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, index=True)
    password = Column(String(45))
    role = Column(SmallInteger)

    # Relación con la tabla de slices
    slices = relationship("Slices", back_populates="users")
    logs = relationship("Logs", back_populates="users")


class Logs(Base):
    __tablename__ = "logs"  # Corregir el nombre de la tabla

    idLogs = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc = Column(LargeBinary, nullable=False)  # Corregir el tipo de datos y permitir que no sea nulo
    idUsers = Column(Integer, ForeignKey('users.idUser'), index=True,
                     nullable=False)  # Corregir la relación con la tabla 'users'

    users = relationship("Users", back_populates="logs")  # Ajustar el nombre de la relación con la clase 'User'


class Slice(Base):
    __tablename__ = 'slices'

    idSlices = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    status = Column(SmallInteger)
    number_nodes = Column(String(45))
    number_links = Column(String(45))
    idUsers = Column(Integer, ForeignKey('users.idUser'))

    # Relación con la tabla de usuarios
    users = relationship("Users", back_populates="slices")
    token = relationship("Token", back_populates="slices")
    nodes = relationship("Nodes", back_populates="slices")


class Node(Base):
    __tablename__ = 'nodes'

    MAC = Column(String(20), primary_key=True)
    VM_name = Column(String(45))
    capacity = Column(String(45))
    port = Column(String(45))
    description = Column(String(45), nullable=True)
    idSlices = Column(Integer, ForeignKey('slices.idSlices'))
    idflavor = Column(Integer, ForeignKey('flavor.idflavor'))

    idImages = Column(Integer, ForeignKey('images.idImages'))
    status = Column(SmallInteger)
    idServers = Column(Integer, ForeignKey('servers.idServers'))

    # Relaciones con otras tablas
    slices = relationship("Slices", back_populates="nodes")
    flavor = relationship("Flavor", back_populates="nodes")
    edges = relationship("Edges", back_populates="nodes")
    images = relationship("Images", back_populates="nodes")
    servers = relationship("Servers", back_populates="nodes")
    sytemsresources = relationship("Sytemsresources", back_populates="nodes")


class Flavor(Base):
    __tablename__ = 'flavor'

    idFlavor = Column(Integer, primary_key=True, index=True)
    memory = Column(String(45))
    RAM = Column(String(45))
    disk = Column(String(45))

    # Relación con la tabla de nodes
    nodes = relationship("Nodes", back_populates="flavor")


class Edge(Base):
    __tablename__ = 'edges'

    idedges = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=True)
    nodes_MAC = Column(String(20), ForeignKey('nodes.MAC'))

    # Relación con la tabla de nodes
    nodes = relationship("Nodes", back_populates="edges")
    subnet = relationship("Subnet", back_populates="edges")


class Subnet(Base):
    __tablename__ = 'subnet'

    idsubnet = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))
    edges_idedges = Column(Integer, ForeignKey('edges.idedges'))

    # Relación con la tabla de edges
    edges = relationship("Edges", back_populates="subnet")
    port = relationship("Port", back_populates="subnet")


class Port(Base):
    __tablename__ = 'port'

    idport = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))
    idSubnet = Column(Integer, ForeignKey('subnet.idsubnet'))

    # Relación con la tabla de subnet
    subnet = relationship("Subnet", back_populates="port")


class Image(Base):
    __tablename__ = 'images'

    idimages = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    plataforma = Column(SmallInteger)
    ruta = Column(String(45), nullable=True)

    nodes = relationship("Nodes", back_populates="images")


class Server(Base):
    __tablename__ = 'servers'

    idServers = Column(Integer, primary_key=True, index=True)
    ServerName = Column(String(45))
    ServerIP = Column(String(45))
    ServerStatus = Column(String(45))
    AZ = Column(SmallInteger)

    nodes = relationship("Nodes", back_populates="servers")


class ServerUsage(Base):
    __tablename__ = 'serverusage'

    idserverusage = Column(Integer, primary_key=True, index=True)
    CPUUsage = Column(String(45))
    MemoryUsage = Column(String(45))
    timestamp = Column(DateTime)
    idServers = Column(Integer, ForeignKey('servers.idServers'))

    # Relación con la tabla de servers
    server = relationship("Server", back_populates="serverusage")


class SystemsResources(Base):
    __tablename__ = 'sytemsresources'

    idsytemsResources = Column(Integer, primary_key=True, index=True)
    CPUUsage = Column(String(45))
    memory = Column(String(45))
    disk = Column(String(45))
    timestamp = Column(String(45))
    MAC = Column(String(12), ForeignKey('nodes.MAC'))

    # Relación con la tabla de nodes
    nodes = relationship("Nodes", back_populates="sytemsresources")
