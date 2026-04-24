# RIEGO IoT Backend 🌿

Este es el backend modular del sistema **RIEGO**, diseñado para la gestión y automatización de sistemas de riego hidropónico utilizando Django y Django REST Framework.


## 🛠️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en un nuevo entorno:

### 1. Clonar el repositorio
```bash
git clone https://github.com/robertoguillot1/backend_profesor.git
cd backend_profesor
```

### 2. Crear un entorno virtual
```bash
python -m venv venv
```

### 3. Activar el entorno virtual
*   **En Windows:**
    ```bash
    venv\Scripts\activate
    ```
*   **En Linux/Mac:**
    ```bash
    source venv/bin/activate
    ```

### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. Ejecutar el servidor
```bash
python manage.py runserver
```

---

## 📂 Estructura del Proyecto

El backend está organizado de forma modular para facilitar la escalabilidad:

*   **`modules/farms/`**: Gestión de granjas, zonas y parcelas.
*   **`modules/devices/`**: Administración de dispositivos IoT, sensores y actuadores.
*   **`modules/automation/`**: Lógica de comandos, alertas y servicios de automatización.
*   **`modules/core/`**: Funcionalidades compartidas y modelos base.

## 🧪 Pruebas y Simulación
El proyecto incluye scripts para facilitar el desarrollo:
*   `populate_data.py`: Carga datos iniciales de prueba.
*   `simulate_automation.py`: Simula el comportamiento de los actuadores y sensores.

---
Desarrollado por [Roberto Guillot](https://github.com/robertoguillot1)
