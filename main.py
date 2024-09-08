import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="oci.tessa.ooo",
    user="cs425user",
    password="dL5EFJB5nu",
    database="InventoryManagement"
)
c = conn.cursor()

# Function to execute complex SQL queries
def execute_query(query):
    try:
        # Execute the SQL query
        c.execute(query)

        # Fetch all results
        results = c.fetchall()

        # Display the results in the result label
        result_text = ""
        for row in results:
            result_text += ", ".join(str(cell) for cell in row) + "\n"
        result_label.config(text=result_text)
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error executing SQL query: {e}")

# Function to create a new product
def create_product():
    try:
        # Get input values from entry fields
        product_name = product_name_entry.get()
        description = description_entry.get()
        quantity_available = int(quantity_available_entry.get())
        price = float(price_entry.get())
        category_id = int(category_id_entry.get())
        supplier_id = int(supplier_id_entry.get())

        # Insert new product into the database
        query = "INSERT INTO Product (ProductName, Description, QuantityAvailable, Price, CategoryID, SupplierID) VALUES (%s, %s, %s, %s, %s, %s)"
        c.execute(query, (product_name, description, quantity_available, price, category_id, supplier_id))
        conn.commit()
        messagebox.showinfo("Success", "Product created successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Error creating product: {e}")

# Function to read product information
def read_product():
    try:
        # Get input value from entry field
        product_id = int(product_id_entry.get())

        # Retrieve product information from the database
        query = "SELECT * FROM Product WHERE ProductID = %s"
        c.execute(query, (product_id,))
        product_info = c.fetchone()

        # Display product information in a label
        if product_info:
            result_label.config(text=f"Product Name: {product_info[1]}, Description: {product_info[2]}, Quantity Available: {product_info[3]}, Price: {product_info[4]}, CategoryID: {product_info[5]}, SupplierID: {product_info[6]}")
            clear_fields()
        else:
            messagebox.showerror("Error", "Product not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading product: {e}")

# Function to update product quantity
def update_product():
    try:
        # Get input values from entry fields
        product_id = int(product_id_entry.get())
        new_quantity = int(new_quantity_entry.get())

        # Update product quantity in the database
        query = "UPDATE Product SET QuantityAvailable = %s WHERE ProductID = %s"
        c.execute(query, (new_quantity, product_id))
        conn.commit()
        messagebox.showinfo("Success", "Product quantity updated successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Error updating product: {e}")

# Function to delete a product
def delete_product():
    try:
        # Get input value from entry field
        product_id = int(product_id_entry.get())

        # Delete product from the database
        query = "DELETE FROM Product WHERE ProductID = %s"
        c.execute(query, (product_id,))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting product: {e}")

# Function to clear all entry fields
def clear_fields():
    product_name_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    quantity_available_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    category_id_entry.delete(0, tk.END)
    supplier_id_entry.delete(0, tk.END)
    new_quantity_entry.delete(0, tk.END)
    product_id_entry.delete(0, tk.END)

# Function to execute custom SQL queries
def execute_custom_query():
    # Get input value from entry field
    custom_query = custom_query_entry.get()

    # Execute custom SQL query
    execute_query(custom_query)

# Predefined advanced queries
def predefined_query_1():
    query = """
        -- Predefined Advanced Query 1: List of products with low stock
        SELECT ProductID, ProductName, Description, QuantityAvailable, Price
        FROM Product
        WHERE QuantityAvailable < 50
        ORDER BY QuantityAvailable ASC
        LIMIT 10;
    """
    execute_query(query)

def predefined_query_2():
    query = """
        -- Predefined Advanced Query 2: Total sales by category
        SELECT CategoryID, SUM(Price * QuantityAvailable) AS TotalSales
        FROM Product
        GROUP BY CategoryID;
    """
    execute_query(query)

def predefined_query_3():
    query = """
        -- Predefined Advanced Query 3: Top suppliers
        SELECT SupplierID, COUNT(*) AS TotalProducts
        FROM Product
        GROUP BY SupplierID
        ORDER BY TotalProducts DESC
        LIMIT 5;
    """
    execute_query(query)

# Create the main application window
root = tk.Tk()
root.title("Inventory Management Application")

# Create entry fields for user input
product_name_label = tk.Label(root, text="Product Name:")
product_name_label.grid(row=0, column=0)
product_name_entry = tk.Entry(root)
product_name_entry.grid(row=0, column=1)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=1, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1)

quantity_available_label = tk.Label(root, text="Quantity Available:")
quantity_available_label.grid(row=2, column=0)
quantity_available_entry = tk.Entry(root)
quantity_available_entry.grid(row=2, column=1)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=3, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1)

category_id_label = tk.Label(root, text="Category ID:")
category_id_label.grid(row=4, column=0)
category_id_entry = tk.Entry(root)
category_id_entry.grid(row=4, column=1)

supplier_id_label = tk.Label(root, text="Supplier ID:")
supplier_id_label.grid(row=5, column=0)
supplier_id_entry = tk.Entry(root)
supplier_id_entry.grid(row=5, column=1)

new_quantity_label = tk.Label(root, text="New Quantity:")
new_quantity_label.grid(row=6, column=0)
new_quantity_entry = tk.Entry(root)
new_quantity_entry.grid(row=6, column=1)

product_id_label = tk.Label(root, text="Product ID:")
product_id_label.grid(row=7, column=0)
product_id_entry = tk.Entry(root)
product_id_entry.grid(row=7, column=1)

# Label for Basic Queries
basic_queries_label = tk.Label(root, text="Basic Queries", font=("Arial", 12, "bold"))
basic_queries_label.grid(row=8, columnspan=2)

# Create buttons for CRUD operations
create_button = tk.Button(root, text="Create Product", command=create_product)
create_button.grid(row=9, column=0)

read_button = tk.Button(root, text="Read Product", command=read_product)
read_button.grid(row=9, column=1)

update_button = tk.Button(root, text="Update Product", command=update_product)
update_button.grid(row=10, column=0)

delete_button = tk.Button(root, text="Delete Product", command=delete_product)
delete_button.grid(row=10, column=1)

# Separator between CRUD operations and Advanced Queries
separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator.grid(row=11, columnspan=2, sticky="ew", pady=5)

# Label for Advanced Queries
advanced_queries_label = tk.Label(root, text="Advanced Queries", font=("Arial", 12, "bold"))
advanced_queries_label.grid(row=12, columnspan=2)

# Entry field for custom query
custom_query_label = tk.Label(root, text="Custom Query:")
custom_query_label.grid(row=13, column=0)
custom_query_entry = tk.Entry(root)
custom_query_entry.grid(row=13, column=1)

# Create labels to display results
result_label = tk.Label(root, text="")
result_label.grid(row=14, columnspan=2)

# Create buttons for predefined advanced queries
predefined_query_1_button = tk.Button(root, text="Low Stock Products", command=predefined_query_1)
predefined_query_1_button.grid(row=15, column=0)

predefined_query_2_button = tk.Button(root, text="Total Sales by Category", command=predefined_query_2)
predefined_query_2_button.grid(row=15, column=1)

predefined_query_3_button = tk.Button(root, text="Top Suppliers", command=predefined_query_3)
predefined_query_3_button.grid(row=16, column=0)

# Create button for executing custom SQL query
execute_query_button = tk.Button(root, text="Execute Custom Query", command=execute_custom_query)
execute_query_button.grid(row=16, column=1)

# Run the application
root.mainloop()

# Close connection to the database
conn.close()
