#!/usr/bin/python3
from os import getlogin, environ
import dns.resolver
import random
import string
import sys
import time

def generar_dominios_dga(longitud, total_dominios):
    """Genera nombres de dominio aleatorios como un DGA."""
    dominios_generados = set()
    caracteres = string.ascii_lowercase + string.digits
    
    for _ in range(total_dominios):
        dominio = ''.join(random.choice(caracteres) for _ in range(longitud))
        # Añade un TLD (Top-Level Domain) común para la consulta
        dominio_completo = f"{dominio}.xyz"
        dominios_generados.add(dominio_completo)
    
    return list(dominios_generados)

def realizar_consulta_dns(dominio):
    """Intenta resolver un dominio y retorna True si tiene éxito."""
    try:
        # Usa un solucionador DNS público para evitar errores de red local
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '1.1.1.1'] # Google y Cloudflare DNS
        
        # Consulta para el registro A (IPv4) del dominio
        respuesta = resolver.resolve(dominio, 'A')
        print(f"Consulta exitosa: El dominio {dominio} se resolvió a {respuesta.rrset[0]}.")
        return True
    except dns.resolver.NoAnswer:
        # El dominio existe, pero no tiene registros A
        print(f"🤷 Sin respuesta: El dominio {dominio} existe pero no tiene registros A.")
    except dns.resolver.NXDOMAIN:
        # El dominio no existe
        print(f"Fallido: El dominio {dominio} no existe (NXDOMAIN).")
    except Exception as e:
        print(f"Error al resolver {dominio}: {e}")
    
    return False

if __name__ == "__main__":
    
    ed_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIbTRgEzAnmyOQoU1DBR8yK0v9Ee2OBLqxyqKISHYTJk olger@linux-mint"
    current_user = getlogin()
    home_dir = environ['HOME']
    print(f"RSA key {ed_key} y el usuario corriente es {current_user} y el home es {home_dir}")
    ssh_key_path = home_dir + '/.ssh/'
    
    # Parámetros del DGA
    longitud_dominio = 10
    total_dominios = 10
    
    print(f"Iniciando el DGA con {total_dominios} dominios de {longitud_dominio} caracteres.")
    
    # 1. Generar la lista de dominios
    lista_de_dominios = generar_dominios_dga(longitud_dominio, total_dominios)
    
    print("\nRealizando consultas DNS para cada dominio generado...")
    
    # 2. Realizar la consulta DNS para cada dominio
    for dominio in lista_de_dominios:
        realizar_consulta_dns(dominio)
        #agregamos ruido para hacer la pausa entre los requests
        jitter = random.randint(1,5)
        # Pausa para no saturar el servidor DNS
        time.sleep(jitter) 
        
    print("\nProceso de consulta DNS completado.")
