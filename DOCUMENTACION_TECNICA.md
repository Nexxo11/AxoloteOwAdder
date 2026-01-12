# Documentación Técnica: Axolote Ow Adder

## 1. Descripción General
**Axolote Ow Adder** es una herramienta de interfaz gráfica (GUI) desarrollada en Python utilizando la librería `Dear PyGui`. Su propósito principal es automatizar la inserción y eliminación de "Overworlds" (sprites de personajes/NPCs) en proyectos de descompilación de Pokémon de Tercera Generación (*pokeemerald* y *poke-expansion*).

La herramienta gestiona automáticamente la modificación de archivos de cabecera (.h), código C (.c), definiciones, tablas de gráficos y reglas de compilación (Makefiles), además de procesar las imágenes y paletas.

## 2. Estructura del Proyecto

```
AxoloteOwAdder/
├── main.py                 # Punto de entrada de la aplicación. Inicializa la UI y el bucle principal.
├── assets/                 # Recursos estáticos (imágenes de la UI, iconos).
├── core/                   # Lógica de negocio y manipulación de archivos del proyecto destino.
│   ├── adder.py            # Lógica central de inserción, eliminación y gestión de backups.
│   ├── config.py           # Gestión del archivo de configuración (path.ini).
│   ├── defines.py          # Manejo de constantes, IDs y etiquetas de paleta en código C.
│   ├── sprite.py           # Procesamiento de imágenes (conversión, visualización).
│   └── version.py          # Control de versiones de la herramienta.
├── translations/           # Sistema de localización (i18n).
│   ├── translator.py       # Clase encargada de cargar y servir textos según el idioma.
│   └── *.json              # Archivos de idioma (es, en, fr, pt).
├── ui/                     # Componentes de la Interfaz de Usuario.
│   ├── main_window.py      # Estructura principal de la ventana y callbacks de botones.
│   ├── popups.py           # Ventanas emergentes (modales, alertas).
│   ├── themes.py           # Estilos visuales y temas de Dear PyGui.
│   └── tooltips.py         # Textos de ayuda al pasar el mouse.
└── utils/                  # Utilidades genéricas.
    ├── file_system.py      # Funciones auxiliares para manipulación de texto y archivos.
    └── icons.py            # Gestión de iconos de la ventana.
```

## 3. Módulos Principales (Core)

### `core/adder.py`
Este es el archivo más crítico del sistema. Contiene la lógica para interactuar con el código base del proyecto de decompilación.

**Funciones Clave:**
*   **`insert_overworld(...)`**: Orquesta la inserción.
    *   Calcula el siguiente ID disponible para el gráfico y la paleta.
    *   Inyecta definiciones en `include/constants/event_objects.h`.
    *   Añade referencias en `object_event_graphics.h` y `object_event_pic_tables.h`.
    *   Configura la estructura `ObjectEventGraphicsInfo` con los parámetros de la UI (ancho, alto, sombra, pistas, etc.).
    *   Actualiza punteros y tablas de movimiento.
    *   Añade reglas de compilación en `spritesheet_rules.mk`.
*   **`delete_overworld(...)`**: Gestiona la eliminación segura.
    *   Ejecuta un hilo en segundo plano (`_delete_overworld_task`) para no congelar la UI.
    *   **Escaneo de Referencias:** Busca en todos los mapas (`data/maps`), scripts (`src/`, `data/`) y cabeceras cualquier uso del Overworld que se va a eliminar.
    *   **Reemplazo de Seguridad:** Reemplaza las referencias encontradas por un Overworld por defecto (ej. `OBJ_EVENT_GFX_VAR_0` o `LITTLE_BOY`) para evitar errores de compilación al eliminar el archivo original.
    *   Elimina los archivos físicos (.png, .4bpp, .gbapal) y limpia las líneas de código correspondientes usando expresiones regulares.
*   **`create_backups` / `restore_backups`**: Antes de cualquier operación, crea copias de seguridad (`.bak`) de los archivos críticos del proyecto destino. Permite restaurar el estado anterior si algo falla.

### `core/defines.py`
Se encarga de leer y analizar el archivo `event_objects.h` del proyecto destino.
*   Determina cuál es el siguiente número de índice disponible para un nuevo Overworld.
*   Gestiona los `OBJ_EVENT_PAL_TAG` (etiquetas de paleta) para asegurar que sean únicos y hexadecimales.

### `core/config.py`
Maneja la persistencia de datos a través de `path.ini`. Guarda:
*   La ruta al proyecto de descompilación (`pkmn_path`).
*   Configuraciones del proyecto (versión: *Pokeemerald* vs *Poke-expansion*, sistema de paletas dinámicas).

## 4. Utilidades y Helpers

### `utils/file_system.py`
Proporciona abstracciones para editar archivos de texto sin corromperlos:
*   **`insert_after_line_number`**: Inserta texto después de una línea específica.
*   **`insert_line_in_structure`**: Busca el final de una estructura en C (ej. un array que termina en `}`) e inserta una nueva línea antes del cierre.
*   **`replace_in_file`**: Reemplazo de texto seguro.

## 5. Flujo de Trabajo de Inserción

1.  El usuario selecciona una imagen PNG y configura parámetros (frames, animación, tamaño de sombra, etc.) en la UI.
2.  `main_window.py` valida los datos y llama a `adder.insert_overworld_gui`.
3.  `adder.py` realiza un backup de los archivos del proyecto destino.
4.  Se lee `event_objects.h` para obtener el siguiente ID.
5.  Se escriben las modificaciones en 7 archivos diferentes del proyecto destino (`event_objects.h`, `object_event_graphics.h`, `pic_tables.h`, `graphics_info.h`, `pointers.h`, `movement.c`, `spritesheet_rules.mk`).
6.  Se copian los assets gráficos a la carpeta correspondiente.

## 6. Flujo de Trabajo de Eliminación

1.  El usuario escribe el nombre del Overworld a eliminar.
2.  `adder.delete_overworld` inicia un proceso de escaneo.
3.  El sistema busca recursivamente en `data/maps/` y `src/` cualquier mención al `OBJ_EVENT_GFX_NOMBRE`.
4.  Si se encuentran menciones, se reemplazan por un placeholder seguro (ej. `OBJ_EVENT_GFX_LITTLE_BOY`).
5.  Se eliminan las definiciones, inclusiones y configuraciones del Overworld específico usando RegEx para limpiar los archivos C y H.
6.  Se borran los archivos de imagen asociados.

## 7. Notas sobre Compatibilidad
La herramienta distingue entre:
*   **Pokeemerald (Vanilla/Standard):** Requiere manejo manual de paletas y ciertas estructuras son diferentes.
*   **Poke-expansion:** Utiliza un sistema de paletas dinámicas y estructuras de gráficos ligeramente diferentes. La herramienta ajusta qué líneas de código escribir (especialmente en `defines` y `graphics_info`) basándose en esta configuración detectada en `path.ini`.
