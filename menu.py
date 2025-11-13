import tkinter as tk 
import login
import producto
import proveedores
import clientes
import sucursal
import ventas
def abrir_menu():
    menu= tk.Tk()
    menu.title("Menu Principal")
    menu.geometry("300x250")

    def regresar_a_login():
        menu.destroy()
        login.mostrar_login()
        
    def abrir_productos():
        menu.withdraw()
        ventana_producto = producto.abrir_producto()
        ventana_producto.wait_window()
        menu.deiconify()
    def abrir_proveedores():
        menu.withdraw()
        ventana_proveedores = proveedores.abrir_proveedores()
        ventana_proveedores.wait_window()
        menu.deiconify() 
    
    def abrir_clientes():
        menu.withdraw()
        ventana_clientes = clientes.abrir_clientes()
        ventana_clientes.wait_window()
        menu.deiconify()
    def abrir_sucursal():
        menu.withdraw()
        ventana_sucursal  =sucursal .abrir_sucursal()
        ventana_sucursal.wait_window()
        menu.deiconify()              
        
    def abrir_ventas():
        menu.withdraw()
        ventana_ventas=ventas.abrir_ventas()
        ventana_ventas.wait_window()
        menu.deiconify()
            
    tk.Label(menu, text="Bienvenido al Menu Principal", font=("Arial", 14)).pack(pady=20)
    tk.Button(menu,text="productos",width=25,command=abrir_productos).pack(pady=5)
    tk.Button(menu,text="proveedores",width=25,command=abrir_proveedores).pack(pady=5)
    tk.Button(menu,text="clientes",width=25,command=abrir_clientes).pack(pady=5)
    tk.Button(menu,text="sucursales",width=25,command=abrir_sucursal).pack(pady=5)
    tk.Button(menu,text="ventas",width=25,command=abrir_ventas).pack(pady=5)
    tk.Button(menu,text="Cerrar sesion",width=25,command=regresar_a_login).pack(pady=20)
    menu.mainloop()
if __name__=="__mani__":
    abrir_menu()                