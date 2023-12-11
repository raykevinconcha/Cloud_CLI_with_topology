from sqlalchemy.orm import Session

from models import Node, Slice, Flavor, Edge, Subnet, Port, Image, Server, ServerUsage, SystemsResources

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


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.idUser == user_id).first()


def get_node(db: Session, mac: str):
    return db.query(Node).filter(Node.MAC == mac).first()


def get_flavor(db: Session, flavor_id: int):
    return db.query(Flavor).filter(Flavor.idFlavor == flavor_id).first()


def get_edge(db: Session, edge_id: int):
    return db.query(Edge).filter(Edge.idedges == edge_id).first()


def get_subnet(db: Session, subnet_id: int):
    return db.query(Subnet).filter(Subnet.idsubnet == subnet_id).first()


def get_port(db: Session, port_id: int):
    return db.query(Port).filter(Port.idport == port_id).first()


def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.idimages == image_id).first()


def get_all_images(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Image).offset(skip).limit(limit).all()


def get_server(db: Session, server_id: int):
    return db.query(Server).filter(Server.idServers == server_id).first()


def get_all_servers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Server).offset(skip).limit(limit).all()


def get_serverusage(db: Session, serverusage_id: int):
    return db.query(ServerUsage).filter(ServerUsage.idserverusage == serverusage_id).first()


def get_all_serverusage(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ServerUsage).offset(skip).limit(limit).all()


def get_systemsresources(db: Session, systemsresources_id: int):
    return db.query(SystemsResources).filter(SystemsResources.idsystemsResources == systemsresources_id).first()


def get_all_systemsresources(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SystemsResources).offset(skip).limit(limit).all()


def get_slice(db: Session, slice_id: int):
    return db.query(Slice).filter(Slice.idSlices == slice_id).first()


def get_all_slices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Slice).offset(skip).limit(limit).all()
