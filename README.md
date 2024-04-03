## Control de servicios LAMP

Este pequeño script en Python sirve, básicamente, para realizar un control básico de los servicios que funcionan en la pila LAMP (Apache2 y MariaDB o MySQL). Además permite iniciar phpmyadmin en el navegador y también permite abrir la MySQL o MaríaDB, 
según lo que esté instalado en el equipo. Supongo que esto es evidente, pero este script no instala nada, si quieres instalar LAMP en Ubuntu, tendrás que hacerlo de otra manera.

![control-servicio-lamp](https://github.com/sapoclay/control-servicio-lamp/assets/6242827/503c42bb-1f70-4484-b9bb-59db5e9cc2f5)

Solo es necesario iniciar el script con Python3, y a correr.

El archivo .desktop, es un acceso directo para colocarlo en ~/.local/share/applications/ y así poder utilizarlo desde el menú de actividades de Ubuntu. Evidentemente, las rutas que contiene este archivo, que cada uno las actualice según sus necesidades y donde coloque los archivos correspondientes.

Esto todavía hay que actualizarlo para corregir algunos errores menores, pero es totalmente funcional en Ubuntu 22.04 (que es donde lo utilizo)
