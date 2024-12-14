# Manejador de Finanzas

## Descripción del Proyecto

Este proyecto es una aplicación web para la gestión de finanzas personales. Permite a los usuarios registrar ingresos, egresos, deudas con base en rubros, descripciones, cantidad, y fecha. Ademas permite visualizar mediante graficas la relacion tiempo, rubro y monto. La aplicación está dividida en un backend desarrollado en python con Flask, el frontend  HTML, CSS y JavaScript.

#### Nombre de la WebApp
**MonKey**, La razón del nombre deriva de sobreponer la palabra *Money* y *Key*, siendo que la aplicación busca ser clave con el manejo del dinero, de ahí el nombre

## Uso
Asegurarse de haber instalado docker. [Checar el proceso de instalacion](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-es&ved=2ahUKEwiY47fCq6aKAxUXLkQIHQt2ILQQFnoECCIQAQ&usg=AOvVaw3O3jGiUVGuVzAyR891Kjf7).
Una vez instalado y condigurado docker, situares en la carpeta principal `Manejador-de-Finanzas`. El proceso de generacion de contenedores por primera vez requiere descargar dependencias, versiones especificas con las cuales opera el sistema, asegurarse de tener una conexion a internet estable, de preferencia no publica. Una vez contempaldo esos requisitos realizar los siguiente pasos:<br></br>
  - 1.- Abrir una terminal, donde se encuentre situado en `Manejador-de-Finanzas`.
  - 1.- Ejecutar `docker compose up --build` o bien `docker-compose up--build`, dependiendo del tipo de version que se haya instalado.
  - 2.- Una vez ejecutado, situarse en la direccion IP correspondiente al `js-server`, luego abrirla en el navegador de su preferencia.
  - 3.- Podra visualizar la interfaz de inicio, hacer el proceso de registro.
  - 4.- Si requiere cerrar la aplicacion, en la terminal donde se encuentra corriendo la aplicacion presionar Ctrl-c.
  - 5.- Si requiere levantar la aplicacion solo necesita ejecutar `docker compose up` o bien `docker-compose up`.
  


