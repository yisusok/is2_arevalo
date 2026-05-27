import json
import sys

def main():
    jsonfile = "sitedata.json"
    
    # Lógica condicional para asignar la clave dinámicamente
    if len(sys.argv) > 1:
        jsonkey = sys.argv[1]
    else:
        jsonkey = "token1" # Valor por defecto si no hay argumentos
    
    try:
        with open(jsonfile, "r") as myfile:
            data = myfile.read()
            obj = json.loads(data)
            print(str(obj[jsonkey]))
    except FileNotFoundError:
        print(f"Error: El archivo {jsonfile} no fue encontrado.")
    except KeyError:
        print(f"Error: La clave '{jsonkey}' no existe en el archivo JSON.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {jsonfile} no tiene un formato JSON válido.")

if __name__ == "__main__":
    main()