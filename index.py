import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import webbrowser

class LAMPControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Control de Servicios LAMP") # Título de la ventana
        master.geometry("700x400")  # Ajusta el tamaño de la ventana

        # Establece el icono de la ventana
        icon_image = tk.PhotoImage(file="lamp.png")
        master.iconphoto(True, icon_image)

        # Frame para botones de inicio/detención
        control_frame = tk.Frame(master)
        control_frame.pack(pady=10, side="top", anchor="center")

        # Frame para mensajes de estado
        status_frame = tk.Frame(master)
        status_frame.pack(pady=10, side="top", anchor="center")

        # Frame para la versión de PHP
        php_frame = tk.Frame(master)
        php_frame.pack(pady=10, side="top", anchor="center")

        # Botones de inicio y detención de LAMP
        self.start_lamp_button = tk.Button(control_frame, text="Iniciar LAMP", command=self.start_lamp)
        self.start_lamp_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_lamp_button = tk.Button(control_frame, text="Detener LAMP", command=self.stop_lamp)
        self.stop_lamp_button.grid(row=0, column=1, padx=5, pady=5)
        self.restart_lamp_button = tk.Button(control_frame, text="Reiniciar LAMP", command=self.restart_lamp)
        self.restart_lamp_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Botones de inicio y detención de Apache
        self.start_apache_button = tk.Button(control_frame, text="Iniciar Apache", command=self.start_apache)
        self.start_apache_button.grid(row=1, column=0, padx=5, pady=5)
        self.stop_apache_button = tk.Button(control_frame, text="Detener Apache", command=self.stop_apache)
        self.stop_apache_button.grid(row=1, column=1, padx=5, pady=5)
        self.restart_apache_button = tk.Button(control_frame, text="Reiniciar Apache", command=self.restart_apache)
        self.restart_apache_button.grid(row=1, column=2, padx=5, pady=5)

        # Botones de inicio y detención de MySQL/MariaDB
        self.start_db_button = tk.Button(control_frame, text="Iniciar MySQL/MariaDB", command=self.start_db)
        self.start_db_button.grid(row=2, column=0, padx=5, pady=5)
        self.stop_db_button = tk.Button(control_frame, text="Detener MySQL/MariaDB", command=self.stop_db)
        self.stop_db_button.grid(row=2, column=1, padx=5, pady=5)
        self.restart_db_button = tk.Button(control_frame, text="Reiniciar MySQL/MariaDB", command=self.restart_db)
        self.restart_db_button.grid(row=2, column=2, padx=5, pady=5)

        # Botón para abrir phpMyAdmin
        self.open_phpmyadmin_button = tk.Button(control_frame, text="Abrir phpMyAdmin", command=self.open_phpmyadmin)
        self.open_phpmyadmin_button.grid(row=3, column=0, padx=5, pady=5)

        # Botón para abrir terminal MySQL/MariaDB
        self.open_mysql_terminal_button = tk.Button(control_frame, text="Abrir Terminal MySQL/MariaDB", command=self.open_mysql_terminal)
        self.open_mysql_terminal_button.grid(row=3, column=1, padx=5, pady=5)

        # Etiqueta para mostrar el estado de LAMP
        self.lamp_status_label = tk.Label(status_frame, text="Estado de LAMP: Desconocido", font=("Arial", 12))
        self.lamp_status_label.pack(pady=5)

        # Etiqueta para mostrar la versión de PHP
        php_version_label = tk.Label(php_frame, text="Versión de PHP instalada:", font=("Arial", 12))
        php_version_label.pack(pady=5)

        php_version = self.get_php_version()
        php_version_display = tk.Label(php_frame, text=php_version, font=("Arial", 12))
        php_version_display.pack(pady=5)
        
        # Actualizar estatus
        self.update_status()

    # Método para iniciar LAMP
    def start_lamp(self):
        password = self.ask_password()
        if password:
            self.start_apache(password)
            self.start_db(password)
            self.show_status_message("LAMP iniciado", "green")
            self.update_status()

    # Método para detener LAMP
    def stop_lamp(self):
        password = self.ask_password()
        if password:
            self.stop_apache(password)
            self.stop_db(password)
            self.show_status_message("LAMP detenido", "red")
            self.update_status()

    # Método para iniciar Apache
    def start_apache(self, password=None):
        self.execute_command("sudo systemctl start apache2", password)
        self.show_status_message("Apache iniciado", "green")

    # Método para detener Apache
    def stop_apache(self, password=None):
        self.execute_command("sudo systemctl stop apache2", password)
        self.show_status_message("Apache detenido", "red")

    # Método para iniciar la base de datos (MySQL/MariaDB)
    def start_db(self, password=None):
        if self.is_service_installed("mariadb"):
            service = "mariadb"
        elif self.is_service_installed("mysql"):
            service = "mysql"
        else:
            self.show_status_message("No se encontró MySQL o MariaDB instalado.")
            return

        self.execute_command(f"sudo systemctl start {service}", password)
        self.show_status_message(f"{service.capitalize()} iniciado", "green")

    # Método para detener la base de datos (MySQL/MariaDB)
    def stop_db(self, password=None):
        if self.is_service_installed("mariadb"):
            service = "mariadb"
        elif self.is_service_installed("mysql"):
            service = "mysql"
        else:
            self.show_status_message("No se encontró MySQL o MariaDB instalado.")
            return

        self.execute_command(f"sudo systemctl stop {service}", password)
        self.show_status_message(f"{service.capitalize()} detenido", "red")

    # Método para reiniciar LAMP
    def restart_lamp(self):
        self.stop_lamp()
        self.start_lamp()

    # Método para reiniciar Apache
    def restart_apache(self):
        self.stop_apache()
        self.start_apache()

    # Método para reiniciar la base de datos (MySQL/MariaDB)
    def restart_db(self):
        self.stop_db()
        self.start_db()
        
    # Método para abrir phpMyAdmin en el navegador web
    def open_phpmyadmin(self):
        webbrowser.open('http://localhost/phpmyadmin')

    # Método para abrir la terminal MySQL/MariaDB
    def open_mysql_terminal(self):
        if self.is_service_installed("mariadb"):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "mysql -u root -p"])
        elif self.is_service_installed("mysql"):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "mysql -u root -p"])
        else:
            messagebox.showerror("Error", "No se encontró MySQL o MariaDB instalado.")

    # Método para introducir la contraseña (para iniciar LAMP)
    def ask_password(self):
        password = simpledialog.askstring("Contraseña", "Introduce tu contraseña:", show="*")
        return password

    # Método para mostrar mensajes de estado con opción de cambiar el color del texto
    def show_status_message(self, message, color="blue"):
        self.lamp_status_label.config(text=message, fg=color)
        messagebox.showinfo("Mensaje", message)  # Utilizar messagebox para mostrar un mensaje informativo en un popup
    
    # Método para actualizar el estado de los servicios al iniciar la aplicación
    def update_status(self):
        lamp_status = self.get_lamp_status()
        self.show_status_message("Estado de LAMP: " + lamp_status)

    # Método para obtener el estado de LAMP
    def get_lamp_status(self):
        lamp_status = "Desactivado"
        apache_status = self.get_service_status("apache2")
        db_status = self.get_service_status("mariadb") or self.get_service_status("mysql")
        
        if apache_status and db_status:
            lamp_status = "Activado (Apache y MySQL/MariaDB)"
        elif apache_status:
            lamp_status = "Activado (Apache)"
        elif db_status:
            lamp_status = "Activado (MySQL/MariaDB)"

        return lamp_status

    # Método para obtener el estado de un servicio dado su nombre
    def get_service_status(self, service):
        try:
            subprocess.run(["systemctl", "is-active", "--quiet", service], check=True)
            return True
        except subprocess.CalledProcessError:
            return False


    # Método para comprobar si el servicio (de BD) está instalado
    def is_service_installed(self, service):
        try:
            subprocess.run(["which", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # Método para ejecutar los comandos
    def execute_command(self, command, password=None):
        try:
            if password:
                command = f"echo '{password}' | sudo -S {command}"
            subprocess.run(command, shell=True, check=True)
            print("Comando ejecutado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")

    # Método para obtener la versión de PHP instalada
    def get_php_version(self):
        try:
            php_version = subprocess.check_output(["php", "-v"]).decode("utf-8").strip()
            return php_version
        except subprocess.CalledProcessError:
            return "No se pudo obtener la versión de PHP"

def main():
    root = tk.Tk()
    app = LAMPControlApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()