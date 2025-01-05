"""
Product Registration and Listing System Documentation

This system is developed in Python using the Tkinter library for the graphical user interface (GUI) and SQLite for data persistence. It allows for product registration with name, description, value, and availability, in addition to providing full listing and listing sorted by value.

Tools Used:
- Python: Main programming language.
- Tkinter: Standard Python library for creating graphical interfaces.
- SQLite: Embedded database management system in Python for data storage.
- ttk (Tkinter Treeview): Used to display data in table format.

Features:
1. Product Registration: Allows the insertion of new products into the database with fields for name, description, value, and availability.
2. Full Listing: Displays all registered products in a separate interface, with all detailed information.
3. Sorted Listing by Value: Presents a reduced listing of products, sorted by value, displaying only the name and value of the product.

Code Organization:
- Connection to the SQLite database.
- Definition of main functions for product manipulation (registration and listing).
- Configuration and presentation of the graphical interface with input fields, labels, and action buttons.
- Use of Treeview for displaying the registered products.

How to Use:
1. Run the Python script to open the system interface.
2. Fill in the fields for name, description, value, and availability to register a new product.
3. Use the buttons to access the full listing or the listing sorted by value.

Notes:
- Ensure that the 'database.db' file is in the same directory as the script or it will be created automatically.
- Changes to the database are immediately persisted after each registration operation.

This system is a basic solution for product management and can be expanded with additional features as needed.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Connection to the SQLite database
# ----------------------------------------------------------------------------
database = sqlite3.connect("database.db")

cursor = database.cursor()

# Create the products table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS produtos (nome TEXT, descricao TEXT, valor TEXT, disponivel TEXT)")

# Function to list all products in a new window
# ----------------------------------------------------------------------------
def list_products():
    # Configure the listing frame
    listing_frame.place(relheight=1, relwidth=1)

    # Select all products from the database
    products = cursor.execute("SELECT * FROM produtos")

    # Remove all existing items from the Treeview
    for item in listing.get_children():
        listing.delete(item)
    
    # Configure the columns of the listing Treeview
    listing.column('nome', width=120)
    listing.column('descricao', width=200)
    listing.column('valor', width=90)
    listing.column('disponivel', width=90)

    # Insert each product into the Treeview
    for p in products:
        listing.insert('', 'end', values=p)

    # Display the Treeview and the back button
    listing.place(x=100, y=50, width=800)

    backHomeBt = tk.Button(listing_frame, text="Back", command= lambda: listing_frame.place_forget())
    backHomeBt.place(x=1, y=1)

# Function to list products sorted by value (specific columns)
# ----------------------------------------------------------------------------
def collumnListingProducts():
    # Select products sorted by value converted to REAL
    products = cursor.execute("SELECT * FROM produtos ORDER BY CAST(valor AS REAL) ASC")

    # Remove all existing items from the Treeview
    for item in collumnListing.get_children():
        collumnListing.delete(item)
    
    # Configure the columns of the reduced listing Treeview
    collumnListing.column('nome', width=120)
    collumnListing.column('valor', width=100)

    # Insert each product into the Treeview with name and value
    for p in products:
        collumnListing.insert('', 'end', values=(p[0], p[2]))
    collumnListing.place(x=800, y=200, width=400)

# Function to register a new product
# ----------------------------------------------------------------------------
def register():
    # Get the data from the input fields
    productName = name.get().strip().title()
    productDescription = description.get().strip().title()
    productValue = value.get().replace(',', '.').strip()
    productAvailable = available.get().title()

    # Check if all fields are filled correctly
    if productName and productDescription and productValue and productAvailable in ["Yes", "No"]:
        try:
            # Attempt to convert the value to float
            productValue = float(productValue)
        except:
            # Display error message if the conversion fails
            messagebox.showerror("Error", "Invalid value!")
        else:
            # Insert the product into the database
            cursor.execute("INSERT INTO produtos (nome, descricao, valor, disponivel) VALUES (?, ?, ?, ?)", (productName, productDescription, productValue, productAvailable,))
            
            # Clear the input fields
            name.delete(0, tk.END)
            description.delete(0, tk.END)
            value.delete(0, tk.END)
            available.set('')
            
            # Commit the changes to the database
            database.commit()
            messagebox.showinfo("Completed", "Product added successfully!")
    else:
        # Display error message if any field is incorrect
        messagebox.showerror("Error", "Fill in all fields correctly!")
    
    # Update the reduced product listing
    collumnListingProducts()

# Initial Tkinter configuration
# ----------------------------------------------------------------------------
app = tk.Tk()
app.title("Product Registration and Listing")
app.geometry("900x500")

# Input fields and labels for product registration
# ----------------------------------------------------------------------------
nameLb = tk.Label(app, text= "Product Name:")
nameLb.place(x=60,y=60)
name = tk.Entry(app, width=30)
name.place(x=200,y=60)

descriptionLb = tk.Label(app, text= "Product Description:")
descriptionLb.place(x=60,y=100)
description = tk.Entry(app, width=60)
description.place(x=200,y=100)

valueLb = tk.Label(app, text="Product Value:")
valueLb.place(x=600,y=60)
value = tk.Entry(app)
value.place(x=700,y=60)

availableLb = tk.Label(app, text="Available:")
availableLb.place(x=600,y=100)
available = ttk.Combobox(app, width=30)
available['values'] = ["Yes", "No"]
available.place(x=700,y=100)

# Treeview for reduced listing with Name and Value
# ----------------------------------------------------------------------------
collumnListing = ttk.Treeview(app, columns=("nome","valor"), show='headings')
collumnListing.heading('nome', text='Product Name', anchor="w")
collumnListing.heading('valor', text='Value', anchor="w")

# Action buttons
# ----------------------------------------------------------------------------
registerBt = tk.Button(app, text="Register", command=register)
registerBt.place(x=200, y=200)

listBt = tk.Button(app, text="Full Listing", command=list_products)
listBt.place(x=300, y=200)

# Frame and Treeview for full product listing
# ----------------------------------------------------------------------------
listing_frame = tk.Frame(app)

listing = ttk.Treeview(listing_frame, columns=("nome","descricao","valor", "disponivel"), show='headings')
listing.heading('nome', text='Product Name', anchor='center')
listing.heading('descricao', text='Description', anchor='center')
listing.heading('valor', text='Value', anchor='center')
listing.heading('disponivel', text='Available', anchor='center')

# Initialize the reduced product listing
collumnListingProducts()

# Start the Tkinter main loop
# ----------------------------------------------------------------------------
app.mainloop()
database.close()  # Close the database connection when finished
