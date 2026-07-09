from ncclient import manager
import xml.dom.minidom

# Datos de conexión al router
HOST = "192.168.56.108"
PORT = 830  # puerto estándar de NETCONF
USUARIO = "admin"
PASSWORD = "cisco123"  # reemplaza por tu contraseña real del router

def conectar():
    """Establece la conexión NETCONF con el router"""
    return manager.connect(
        host=HOST,
        port=PORT,
        username=USUARIO,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'csr'},
        allow_agent=False,
        look_for_keys=False
    )


def cambiar_hostname(conn, nuevo_nombre):
    """Cambia el nombre del router usando NETCONF"""
    config_xml = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>{nuevo_nombre}</hostname>
        </native>
    </config>
    """
    respuesta = conn.edit_config(target="running", config=config_xml)
    print(f"Hostname cambiado a: {nuevo_nombre}")
    print(respuesta)


def crear_loopback(conn, numero, ip, mascara):
    """Crea una interfaz loopback con IP asignada"""
    config_xml = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>{numero}</name>
                    <ip>
                        <address>
                            <primary>
                                <address>{ip}</address>
                                <mask>{mascara}</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
            </interface>
        </native>
    </config>
    """
    respuesta = conn.edit_config(target="running", config=config_xml)
    print(f"Loopback {numero} creada con IP {ip}/{mascara}")
    print(respuesta)


def main():
    print("=== Conectando al router CSR1000v vía NETCONF ===")
    conn = conectar()
    print("Conexión establecida correctamente.\n")

    # 1. Cambiar el hostname del router (apellido del grupo)
    cambiar_hostname(conn, "Garrido")

    # 2. Crear interfaz Loopback 111 con IP 111.111.111.111/32
    crear_loopback(conn, "111", "111.111.111.111", "255.255.255.255")

    conn.close_session()
    print("\nSesión NETCONF cerrada.")


if __name__ == "__main__":
    main()
