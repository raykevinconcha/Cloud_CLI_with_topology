
from sqlalchemy.orm import Session

from APIS_ALCHEMY import crud
from database import SessionLocal




from typing import List

from schemas import User,Slice,Servers , Node , Edges, Subnet , Port ,Serversusage, Systemsresources

from fastapi import Depends, FastAPI, HTTPException, Request, Response

from crud import  get_all_servers, get_all_slices, get_edge,get_serverusage,get_user,get_server,get_node,get_subnet,get_port,get_all_serverusage,get_all_systemsresources,get_slice,get_systemsresources
from database import SessionLocal, engine  

from OpenStk_func import *

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users =get_user(db, skip=skip, limit=limit)
    return users

# Ruta para obtener información de un usuario y sus slices
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.idUser == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Ruta para obtener todas las slices de un usuario
@app.get("/users/{user_id}/slices", response_model=List[Slice])
def read_slices_by_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.idUser == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    slices = db.query(Slice).join(User).filter(User.idUser == user_id).all()
    return slices

@app.get("/servers/{server_id}", response_model=Servers)
def read_server_route(server_id: int, db: Session = Depends(get_db)):
    server = get_server(db, server_id)
    if server is None:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    return server

@app.get("/servers/", response_model=List[Servers])
def read_all_servers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_servers(db, skip=skip, limit=limit)



@app.get("/nodes/{mac}", response_model=Node)
def read_node_route(mac: str, db: Session = Depends(get_db)):
    node = get_node(db, mac)
    if node is None:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    return node

@app.get("/edges/{edge_id}", response_model=Edges)
def read_edge_route(edge_id: int, db: Session = Depends(get_db)):
    edge = get_edge(db, edge_id)
    if edge is None:
        raise HTTPException(status_code=404, detail="Edge no encontrado")
    return edge

@app.get("/subnets/{subnet_id}", response_model=Subnet)
def read_subnet_route(subnet_id: int, db: Session = Depends(get_db)):
    subnet = get_subnet(db, subnet_id)
    if subnet is None:
        raise HTTPException(status_code=404, detail="Subnet no encontrado")
    return subnet

@app.get("/ports/{port_id}", response_model=Port)
def read_port_route(port_id: int, db: Session = Depends(get_db)):
    port = get_port(db, port_id)
    if port is None:
        raise HTTPException(status_code=404, detail="Port no encontrado")
    return port


@app.get("/serverusage/{serverusage_id}", response_model=Serversusage)
def read_serverusage_route(serverusage_id: int, db: Session = Depends(get_db)):
    serverusage = get_serverusage(db, serverusage_id)
    if serverusage is None:
        raise HTTPException(status_code=404, detail="Registro de uso del servidor no encontrado")
    return serverusage

@app.get("/serverusage/", response_model=List[Serversusage])
def read_all_serverusage(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_serverusage(db, skip=skip, limit=limit)


@app.get("/systemsresources/{systemsresources_id}", response_model=Systemsresources)
def read_systemsresources_route(systemsresources_id: int, db: Session = Depends(get_db)):
    systemsresources = get_systemsresources(db, systemsresources_id)
    if systemsresources is None:
        raise HTTPException(status_code=404, detail="Recursos del sistema no encontrados")
    return systemsresources

@app.get("/systemsresources/", response_model=List[Systemsresources])
def read_all_systemsresources(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_systemsresources(db, skip=skip, limit=limit)


@app.get("/slices/", response_model=List[Slice])
def list_slices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Slice).offset(skip).limit(limit).all()


@app.get("/slices/{slice_id}", response_model=Slice)
def read_slice_route(slice_id: int, db: Session = Depends(get_db)):
    slice = get_slice(db, slice_id)
    if slice is None:
        raise HTTPException(status_code=404, detail="Slice no encontrado")
    return slice

@app.get("/slices/", response_model=List[Slice])
def read_all_slices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_slices(db, skip=skip, limit=limit)


@app.post("/deploy/{id}")
async def desplegar_slice(id: int, db=Depends(get_db)):
    db_slice = crud.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    print("desplegado")

    # 0.- Validar el espacio (monitoreo) obtener id_az que viene con id_slice y luego nombre
    ##zona disponibilidad
    db_availability_zone = db_slice.id_az
    if db_availability_zone == 1:
        db_availability_zone = 'Worker1'
    elif db_availability_zone == 2:
        db_availability_zone = 'Worker2'
    elif db_availability_zone == 3:
        db_availability_zone = 'Worker3'
    flavors = crud_flavor.get_flavors_by_id_slice(db, id_slice=id)
    # zona_disponibilidad = vmplacement.elegir_zonaDisponibilidad(flavors,db_availability_zone)
    zona_disponibilidad = "Worker1"
    if zona_disponibilidad:
        print("La zona disponibilidad es: " + zona_disponibilidad)

        # 1.- Obtener token
        project_name = db_slice.name
        project_description = "-"
        admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP, ADMIN_PASSWORD, ADMIN_USERNAME, ADMIN_DOMAIN_NAME,
                                                  DOMAIN_ID, ADMIN_PROJECT_NAME)
        if admin_token:
            # 2.- Crear el proyecto

            project = openstack.crearProyecto(GATEWAY_IP, admin_token, DOMAIN_ID, project_name, project_description)
            project_id = project["project"]["id"]
            openstack.asignarRol(GATEWAY_IP, admin_token, project_id, ADMIN_ID, ADMIN)
            # 3.- Token del proyecto
            # 3.1.-Asignar rol admin al usuario admin
            # 3.2.-Crear usuario y asignar rol al usuario (rol reader) --pendiente--
            project_token = openstack.obtenerTokenProject(GATEWAY_IP, admin_token, DOMAIN_ID, project_name)
            print(project_token)
            # 4.- Creacion de network (network_name es la id)
            links = crud_link.get_link_by_slice(db, id_slice=id)
            links_temp = {}

            for link in links:
                network_name = str(link.id)
                network = openstack.crearRed(GATEWAY_IP, project_token, network_name)

                network_id = network["network"]["id"]
                # 5.- Creación de subnet (subnet name es el id)
                subnet_name = f"Subnet_{link.id}"
                subnet = openstack.crearSubred(GATEWAY_IP, project_token, network_id, subnet_name, IP_VERSION, CIDR)
                subnet_id = subnet["subnet"]["id"]
                # 6.- Creación de puertos
                port_name0 = link.port0.name
                puerto0 = openstack.crearPuerto(GATEWAY_IP, project_token, port_name0, network_id, project_id)
                puerto0_id = puerto0["port"]["id"]
                port_name1 = link.port1.name
                puerto1 = openstack.crearPuerto(GATEWAY_IP, project_token, port_name1, network_id, project_id)
                puerto1_id = puerto1["port"]["id"]

                links_temp[link.id] = {
                    "network": network_id,
                    "subnet": subnet_id,
                    "puerto0": puerto0_id,
                    "puerto1": puerto1_id
                }
            # 7.- Crear las instancias
            # 7.1 Crear Flavors

            flavors = crud_flavor.get_flavors_by_id_slice_distinct(db, id_slice=id)
            for flavor in flavors:
                name = f"Flavor_{flavor.id}"
                ram = flavor.ram
                vcpus = flavor.core
                disk = flavor.disk

                flavor_os = openstack.crearFlavor(GATEWAY_IP, project_token, name, int(ram), vcpus, int(disk),
                                                  flavor.id)

            nodes = crud_node.get_nodes_by_slice(db, slice_id=id)
            nodes_temp = {}

            for node in nodes:
                instance_name = node.name
                flavor_id = node.flavor.id
                networks = []
                for port in node.ports:
                    link = crud_link.get_link_by_port0(db, id_port=port.id)
                    if link is None:
                        link = crud_link.get_link_by_port1(db, id_port=port.id)
                        port = links_temp[link.id]["puerto1"]
                    else:
                        port = links_temp[link.id]["puerto0"]

                    networks.append({"port": port})
                node0 = openstack.crearInstancia(GATEWAY_IP, project_token, instance_name, flavor_id, IMAGEN_ID,
                                                 networks)
        else:
            print('No se pudo obtener el token.')
        return {}