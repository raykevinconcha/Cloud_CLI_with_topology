import paramiko


def execute_script_on_worker1():
    # Datos de conexión al worker1 desde el headnode
    worker1_hostname = '10.0.0.30'
    worker1_port = 22
    worker1_username = 'ubuntu'
    worker1_password = 'ubuntu'  # Reemplaza con tu contraseña

    # Crear una instancia de cliente SSH para el worker1
    worker1_client = paramiko.SSHClient()
    worker1_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conectar al worker1 desde el headnode con contraseña
    worker1_client.connect(worker1_hostname, port=worker1_port, username=worker1_username, password=worker1_password)
    print("conecto al wk1")
    # Ejecutar el script en el worker1
    script_path_on_worker1 = '/home/ubuntu/scripts/nada.sh'  # Reemplaza con la ruta correcta
    command = f'bash {script_path_on_worker1}'
    stdin, stdout, stderr = worker1_client.exec_command(command)
    print("se ejecuto script")

    # Imprimir la salida del comando ejecutado en el worker1
    print(stdout.read().decode())

    # Cerrar la conexión SSH al worker1
    worker1_client.close()


try:
    # Ejecutar el script en el worker1 desde el headnode
    execute_script_on_worker1()
    print("ingreso!")

except Exception as e:
    print(f"Error: {e}")
