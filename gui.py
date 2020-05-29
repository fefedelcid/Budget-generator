from tkinter import Tk, mainloop, Label, Entry, LabelFrame, Button, W, E, \
                    CENTER, Toplevel, StringVar
from tkinter.ttk import Treeview
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, root, h=600, w=800):
        self.root = root
        self.root.title("Presupuestos")
        self.root.config(height=h, width=w)

        # Frame container
        frame = LabelFrame(self.root, text="Registrar nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name input
        Label(frame, text='Nombre').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Price input
        Label(frame, text='Precio').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Button add product
        btn = Button(frame, text='Añadir Producto', command=self.add_product)
        btn.grid(row=3, columnspan=2, sticky= W+E)

        # Output messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)

        # Table
        self.tree = Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        # Buttons
        delete = Button(text='Eliminar', command=self.delete_product)
        delete.grid(row=5, column=0, sticky=W+E)
        update = Button(text='Editar', command=self.edit_product)
        update.grid(row=5, column=1, sticky=W+E)

        # Filling the row
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            result = cursor.execute(query, parameters)
            db.commit()
        return result

    def get_products(self):
        # cleaning table
        records = self.tree.get_children()
        for e in records:
            self.tree.delete(e)

        # quering data
        query = 'SELECT * FROM products ORDER BY name DESC'
        db_rows = self.run_query(query)

        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=f'${row[2]:.2f}')

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO products VALUES(NULL, ?, ?)'
            n = self.name.get()
            parameters = (n, self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = f'El producto {n} ha sido agregado satisfactoriamente.'
        else:
            self.message['text'] = 'El nombre y el precio son requeridos.'

        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Primero debes seleccionar una fila.'
            return
        query = 'DELETE FROM products WHERE name = ?'
        name = self.tree.item(self.tree.selection())['text']
        self.run_query(query, (name,))
        self.message['text'] = f'El elemento {name} ha sido eliminado satisfactoriamente.'
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Primero debes seleccionar una fila.'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title('Editar producto')

        # Old Name
        Label(self.edit_wind, text='Nombre anterior: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='Nuevo nombre: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        # Old Price
        Label(self.edit_wind, text='Precio anterior: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)

        # New Price
        Label(self.edit_wind, text='Nuevo precio: ').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=1, columnspan=2, sticky=W)

    def edit_records(self, new_name, name, new_price, old_price):
        if new_name == '':
            new_name = name
        if new_price == '':
            new_price = old_price.replace('$', '')
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price.replace('$', ''))
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = f'Producto {name} actualizado satisfactoriamente.'
        self.get_products()

if __name__ == '__main__':
    root = Tk()
    Product(root)
    root.mainloop()
