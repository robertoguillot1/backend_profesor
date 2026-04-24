import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend2.settings')
django.setup()

from modules.farms.models import Farm

def check_crud():
    farms = Farm.objects.filter(name="porvenir")
    print(f"Encontradas {farms.count()} granjas con el nombre 'porvenir'.")
    
    if farms.exists():
        farm_to_delete = farms.first()
        print(f"Intentando eliminar la granja: {farm_to_delete.id} - {farm_to_delete.name}")
        try:
            farm_to_delete.delete()
            print("Eliminación exitosa.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
    else:
        print("No se encontró ninguna granja para eliminar.")

if __name__ == "__main__":
    check_crud()
