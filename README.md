# Manejador de Finanzas

## Descripción del Proyecto

Este proyecto es una aplicación web para la gestión de finanzas personales. Permite a los usuarios registrar ingresos, egresos, deudas y visualizar su historial de transacciones. La aplicación está dividida en un backend desarrollado en Flask y un frontend que ahora utiliza HTML, CSS y JavaScript puro.

## Reestructuración del Front End: De Vue a JS+HTML+CSS

El proyecto fue contemplado inicialmente en Vue, sin embargo, por distintas dificultades técnicas he optado por el uso de la tercia mencionada, con el fin de mantener un proyecto más manejable. 

### ¿Por qué el cambio?

1. **Simplicidad y Mantenibilidad**: Al utilizar HTML, CSS y JavaScript puro, se reduce la complejidad del proyecto. Esto facilita la comprensión del código y su mantenimiento, especialmente para desarrolladores que pueden no estar familiarizados con frameworks como Vue.js.

2. **Menor Sobrecarga**: Los frameworks como Vue pueden introducir una sobrecarga en términos de tamaño de la aplicación y tiempo de carga. Al optar por una solución más ligera, se mejora la velocidad de carga y la experiencia del usuario.

3. **Flexibilidad**: Usar JavaScript puro permite una mayor flexibilidad en la implementación de funcionalidades específicas sin la necesidad de seguir las convenciones de un framework. Esto es especialmente útil en un proyecto que puede evolucionar con el tiempo.

4. **Facilidad de Integración**: La integración con el backend en Flask se simplifica al utilizar JavaScript puro, ya que se puede realizar fácilmente mediante llamadas a la API sin la necesidad de configurar un entorno de Vue.

### Estructura del Proyecto

La reestructura comienza en el archivo `Dockerfile.frontend` con el siguiente código:

```dockerfile
FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app
COPY public/ /app

EXPOSE 8080
CMD ["http-server", "/app"]
```

El frontend será una interfaz web simple que consumirá del API del backend usando JS. No se usará frameworks como React o Vue, pero sí de componentes reutilizables con JS puro.

La estructura de páginas es de la siguiente forma:

*   **Registro:** `signup.html` 
*   **Inicio de Sesión:** `login.html` 
*   **Dashboard:** `dashboard.html` Pra ver el balance general, con gráficos y filtros por fecha
*   **Formulario de transacciones:** `transaction.html` Para registrar ingresos, egresos y aplicarles rubros.
*    **debts.html;** `debts.html`
*    **Historial de transacciones:** `history.html` Para ver el historial filtrado por etiquetas o fechas.

Con esto, tras eliminar todo rastro de Vue.js, el proyecto queda de la siguiente forma: 


```
Manejador-de-Finanzas
├── README.md
├── docker
│   ├── Dockerfile.backend      # Dockerfile para el backend en Flask
│   ├── Dockerfile.frontend     # Dockerfile para el nuevo frontend en HTML, CSS, y JavaScript
├── docker-compose.yml          # Configuración para levantar backend, frontend y base de datos con Docker
├── flask                       # Código del backend en Flask
│   ├── __init__.py
│   ├── app.py                  # Código principal de la app Flask
│   ├── db_config.py            # Configuración de la base de datos SQLAlchemy
│   ├── requirements.txt        # Dependencias del backend
│   ├── models                  # Modelos de la base de datos
│   │   ├── __init__.py
│   │   ├── debts.py            # Modelo de deudas
│   │   ├── tags.py             # Modelo de etiquetas
│   │   ├── transactions.py     # Modelo de transacciones
│   │   ├── types.py            # Modelo de tipos de transacción (ingreso/egreso)
│   │   └── users.py            # Modelo de usuarios
│   ├── routes                  # Rutas y lógica de negocio
│       ├── __init__.py
│       ├── login.py            # Ruta para login
│       ├── signup.py           # Ruta para registro
│       └── signout.py          # Ruta para cerrar sesión
├── public                      # Nuevo frontend (reemplaza la carpeta `views`)
│   ├── index.html              # Página principal del frontend
│   ├── css
│   │   └── styles.css          # Estilos para la aplicación
│   ├── js
│   │    └── main.js            # Lógica en JavaScript para interactuar con el backend
│   └── assets                  # Recursos adicionales, I.e. Fotos
├── wait-for-it.sh              # Script para esperar a que el servicio de MySQL esté listo

```

Cómo se vio, el manejo de la parte visual del proyecto quedará en `public`.

## Estructura inicial de la carpeta `public` para el FrontEnd

Esta configuración está sujetas a cambios en caso de ser necesario

```
public
├── index.html                # Página de login
├── signup.html               # Página de registro de usuario
├── dashboard.html            # Página principal después de iniciar sesión
├── transaction.html          # Página para registrar ingresos y egresos
├── debts.html                # Página para ver y registrar deudas
├── history.html              # Página para ver el historial de transacciones
├── admin                     
│   └── admin_dashboard.html  # Interfaz administrativa
├── css
│   ├── styles.css            # Estilos generales
│   └── admin.css             # Estilos específicos para la interfaz administrativa
├── js
│   ├── main.js               # Lógica de autenticación y login
│   ├── signup.js             # Lógica para el registro de usuarios
│   ├── dashboard.js          # Lógica para la página del dashboard
│   ├── transaction.js        # Lógica para el registro de transacciones
│   ├── debts.js              # Lógica para la página de deudas
│   ├── history.js            # Lógica para la página de historial
│   └── admin                 
│       └── admin_dashboard.js # Lógica para el panel administrativo
└── assets                    # Recursos adicionales
```

##  Detalles del Front

### Nombre de la WebApp
**MonKey**, La razón del nombre deriva de sobreponer la palabra *Money* y *Key*, siendo que la aplicación busca ser clave con el manejo del dinero, de ahí el nombre

### Paleta de Colores 
#181C26, #525559, #F2F2F2, #261201 y #A67951


