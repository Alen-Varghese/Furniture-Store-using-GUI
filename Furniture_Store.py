import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from tkinter import scrolledtext

root = tk.Tk()

PRIMARY_COLOR = "#3498db"  # Light blue color for buttons and accents
SECONDARY_COLOR = "#2ecc71"  # Green color for highlights
BACKGROUND_COLOR = "#ecf0f1"  # Light grey background
TEXT_COLOR = "#2c3e50"  # Darker text color
FONT_MAIN = ("Helvetica", 12)
FONT_TITLE = ("Helvetica", 16, "bold")

# Function to connect to the MySQL database using provided credentials
def connect_to_database():
    try:
        # Get username and password from entry fields
        username = username_entry.get()
        password = password_entry.get()

        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Display success message
        messagebox.showinfo("Success", "Connected to MySQL database successfully!")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        # Remove username and password widgets from the screen
        username_label.pack_forget()
        username_entry.pack_forget()
        password_label.pack_forget()
        password_entry.pack_forget()
        connect_button.pack_forget()

        # Display welcome message
        welcome_label.config(text="Welcome to Furniture Store")

        # Create button to fetch and display store details
        store_details_button = tk.Button(root, text="Store Details", command=fetch_store_details, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        store_details_button.pack(pady=12)

        position_button = tk.Button(root, text="Show Employee Details", command=create_position_selection_window, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        position_button.pack(pady=12)

        product_details_button = tk.Button(root, text="Product Details", command=show_product_details, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        product_details_button.pack(pady=12)

        purchase_button = tk.Button(root, text="Purchase", command=make_purchase, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        purchase_button.pack(pady=12)


        recent_purchase_button = tk.Button(root, text="Recent Purchase", command=display_recent_purchase, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        recent_purchase_button.pack(pady=12)

        customer_button = tk.Button(root, text="Customers", command=display_customer_details, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        customer_button.pack(pady=12)

        offers_button = tk.Button(root, text="Offers", command=display_offers, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        offers_button.pack(pady=12)

        feedback_button = tk.Button(root, text="Feedback", command=submit_feedback, 
                                 font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR,
                                 activeforeground="white", relief="flat", bd=0, padx=13, pady=6)
        feedback_button.pack(pady=12)

        def on_enter(event):
            event.widget['background'] = SECONDARY_COLOR

        def on_leave(event):
            event.widget['background'] = PRIMARY_COLOR

# Apply hover effect to buttons
        for button in [store_details_button, position_button, product_details_button, 
                    purchase_button, recent_purchase_button, customer_button, offers_button, feedback_button]:
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

    except mysql.connector.Error as err:
        # Display error message if connection fails
        messagebox.showerror("Error", f"Failed to connect to MySQL database: {err}")


def fetch_cities():
    try:
         # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()
        """Fetch the last word (city) from each store address and return unique city names."""
        mycursor.execute("SELECT DISTINCT SUBSTRING_INDEX(Address, ',', -1) AS City FROM storedetails")
        cities = mycursor.fetchall()
        return [city[0].strip() for city in cities]

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch store details: {err}")


# Function to display store details for the selected city
def show_store_details(city_name, city_window):
    """Fetch and display store details for the selected city."""
    try:
        # Close the city selection window
        city_window.destroy()

        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Query to fetch store details based on city name
        mycursor.execute("SELECT * FROM storedetails WHERE Address LIKE %s", ('%' + city_name,))
        store_details = mycursor.fetchall()

        # Display store details if any records are found
        if store_details:
            for store in store_details:
                messagebox.showinfo(
                    "Store Details", 
                    f"Branch ID: {store[0]}\nStore Branch: {store[1]}\nAddress: {store[2]}\nContact: {store[3]}\nManager ID: {store[4]}"
                )
        else:
            messagebox.showinfo("Store Details", f"No store found with the city '{city_name}'.")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch store details: {err}")


# Function to fetch store details when the button is clicked
def fetch_store_details():
    """Create a window for selecting a city and display store details for that city."""
    
    # Create a new window for selecting city
    city_window = tk.Toplevel(root)
    city_window.title("Select City")

    # Create label and dropdown menu for selecting city
    city_label = tk.Label(city_window, text="Select City:")
    city_label.pack(pady=5)

    # Fetch city names from the database and populate the dropdown
    cities = fetch_cities()
    if not cities:
        messagebox.showwarning("No Cities", "No cities found in the database.")
        city_window.destroy()
        return
    
    city_var = tk.StringVar(city_window)
    city_var.set(cities[0])  # Default city (first city) in the dropdown

    city_combobox = ttk.Combobox(city_window, textvariable=city_var, values=cities)
    city_combobox.pack(pady=5)

    # Create button to execute query based on selected city
    select_button = tk.Button(city_window, text="Select", command=lambda: show_store_details(city_var.get(), city_window))
    select_button.pack(pady=10)


# Function to show employees based on selected position
def show_all_employees():
    # Create a new window for displaying employee details
    employee_window = tk.Toplevel(root)
    employee_window.title("Employee Details")

    # Create a Text widget with a scrollbar to display employee details
    employee_text = scrolledtext.ScrolledText(employee_window, width=70, height=20, wrap=tk.WORD)
    employee_text.pack(pady=10)

    # Get selected position from dropdown menu
    position = position_var.get()

    # Fetch and display employees based on selected position category
    employee_text.insert(tk.END, f"Fetching {position} employees...\n\n")
    fetch_employees(position, employee_text)

def fetch_employees(position, employee_text):
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Determine the query based on the selected position
        if position == "Manager":
            query = """
            SELECT Emp_ID, Emp_Name, Emp_Position, Emp_PhNo, Emp_Email 
            FROM employee 
            WHERE Emp_Position IN ('Manager', 'Assistant Manager', 'Stock Manager', 'Inventory Manager')
            """
        elif position == "Regular":
            query = """
            SELECT Emp_ID, Emp_Name, Emp_Position, Emp_PhNo, Emp_Email 
            FROM employee 
            WHERE Emp_Position NOT IN ('Manager', 'Assistant Manager', 'Stock Manager', 'Inventory Manager')
            """
        else:
            employee_text.insert(tk.END, f"Invalid category: {position}\n")
            return

        # Execute the query
        mycursor.execute(query)
        employees = mycursor.fetchall()

        # Display employee details in the Text widget
        if employees:
            employee_text.insert(tk.END, f"Employee Details for '{position}' category:\n\n")
            for employee in employees:
                employee_text.insert(tk.END, f"Employee ID: {employee[0]}\n")
                employee_text.insert(tk.END, f"Name: {employee[1]}\n")
                employee_text.insert(tk.END, f"Position: {employee[2]}\n")
                employee_text.insert(tk.END, f"Phone Number: {employee[3]}\n")
                employee_text.insert(tk.END, f"Email: {employee[4]}\n")
                employee_text.insert(tk.END, "-" * 50 + "\n")

        else:
            employee_text.insert(tk.END, f"No employees found for the '{position}' category.\n")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch employee details: {err}")
        employee_text.insert(tk.END, f"Error fetching details: {err}\n")


# Function to create the position selection window
def create_position_selection_window():
    # Create a new window for selecting position
    position_window = tk.Toplevel(root)
    position_window.title("Select Position Category")

    # Create label and dropdown menu for selecting position
    position_label = tk.Label(position_window, text="Select Position Category:")
    position_label.pack(pady=5)

    # Dropdown options: Manager (includes all managerial roles), Regular (all non-managerial)
    position_var.set("Manager")  # Default position (can be changed to Regular or Manager)
    position_options = ["Manager", "Regular"]
    position_dropdown = tk.OptionMenu(position_window, position_var, *position_options)
    position_dropdown.pack(pady=5)

    # Create button to fetch and display employees based on selected position
    select_button = tk.Button(position_window, text="Select", command=show_all_employees)
    select_button.pack(pady=10)

position_var = tk.StringVar(root)
position_var.set("Manager")


# Function to show product details based on selection
def show_product_details():
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute SQL query to fetch all product names
        mycursor.execute("SELECT Prod_Name FROM PRODUCT")
        products = mycursor.fetchall()
        product_names = [product[0] for product in products]

        # Create a new window for selecting product
        product_window = tk.Toplevel(root)
        product_window.title("Select Product")

        # Create label and dropdown menu for selecting product
        product_label = tk.Label(product_window, text="Select Product:")
        product_label.pack(pady=5)

        product_var = tk.StringVar(product_window)
        product_var.set(product_names[0])  # Default product

        product_dropdown = tk.OptionMenu(product_window, product_var, *product_names)
        product_dropdown.pack(pady=5)

        # Function to execute when the stock button is clicked
        def show_stock():
            selected_product = product_var.get()
            check_stock_availability(selected_product)

        # Create button to execute query based on selected product
        select_button = tk.Button(product_window, text="Select", command=lambda: show_product(product_var.get()))
        select_button.pack(pady=10)

        # Create button to check stock availability
        stock_button = tk.Button(product_window, text="Check Stock Availability", command=show_stock)
        stock_button.pack(pady=10)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch product details: {err}")

def show_product(product_name):
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        
        # Execute SQL query to fetch product details based on selected product
        mycursor.execute("SELECT Prod_ID, Prod_Name, Prod_Price FROM PRODUCT WHERE Prod_Name = %s", (product_name,))
        product_details = mycursor.fetchone()

        # Display product details
        messagebox.showinfo("Product Details", f"Product ID: {product_details[0]}\nName: {product_details[1]}\nPrice: {product_details[2]}")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        # Create a button to check stock availability
        stock_button = tk.Button(root, text="Check Stock Availability", command=lambda: check_stock_availability(product_name))
        stock_button.pack(pady=10)

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch product details: {err}")

def check_stock_availability(product_name):
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute SQL query to fetch stock availability based on selected product
        mycursor.execute("SELECT Stock_Capacity, Stock_Avail FROM STOCK WHERE Stock_ID = (SELECT StockID FROM PRODUCT WHERE Prod_Name = %s)", (product_name,))
        stock = mycursor.fetchone()

        # Display stock availability
        messagebox.showinfo("Stock Availability", f"Stock Capacity: {stock[0]}\nStock Available: {stock[1]}")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch stock availability: {err}")

# Function to make a purchase

# Functions to fetch product names and prices
def fetch_product_names():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="furniture"
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT Prod_Name FROM product")
        product_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db_connection.close()
        return product_names
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching product names:\n{err}")
        return []

def fetch_product_prices():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="furniture"
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT Prod_Name, Prod_Price FROM product")
        product_prices = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        db_connection.close()
        return product_prices
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching product prices:\n{err}")
        return {}

# Purchase window setup function
def make_purchase():
    purchase_window = tk.Toplevel(root)
    purchase_window.title("Make a Purchase")
    purchase_window.geometry("400x500")

    input_frame = tk.Frame(purchase_window, padx=10, pady=10)
    input_frame.pack(pady=10)

    # Customer Name
    tk.Label(input_frame, text="Customer Name:").grid(row=0, column=0, pady=5, sticky="w")
    customer_name_entry = tk.Entry(input_frame, width=30)
    customer_name_entry.grid(row=0, column=1, pady=5)

    # Contact Number
    tk.Label(input_frame, text="Contact Number:").grid(row=1, column=0, pady=5, sticky="w")
    contact_number_entry = tk.Entry(input_frame, width=30)
    contact_number_entry.grid(row=1, column=1, pady=5)

    # Order ID (Optional, if needed)
    tk.Label(input_frame, text="Order ID:").grid(row=2, column=0, pady=5, sticky="w")
    order_id_entry = tk.Entry(input_frame, width=30)
    order_id_entry.grid(row=2, column=1, pady=5)

    # Fetch product names dynamically
    product_names = fetch_product_names()
    if product_names:
        tk.Label(input_frame, text="Product Name:").grid(row=3, column=0, pady=5, sticky="w")
        global product_name_var
        product_name_var = tk.StringVar(purchase_window)
        product_name_dropdown = tk.OptionMenu(input_frame, product_name_var, *product_names)
        product_name_var.set(product_names[0])  # Default to the first product
        product_name_dropdown.grid(row=3, column=1, pady=5, sticky="w")
    else:
        tk.Label(input_frame, text="Product Name:").grid(row=3, column=0, pady=5, sticky="w")
        tk.Label(input_frame, text="No products available").grid(row=3, column=1, pady=5, sticky="w")

    # Amount
    tk.Label(input_frame, text="Amount:").grid(row=4, column=0, pady=5, sticky="w")
    global amount_entry
    amount_entry = tk.Entry(input_frame, state='readonly', width=30)
    amount_entry.grid(row=4, column=1, pady=5)

    # Quantity
    tk.Label(input_frame, text="Quantity:").grid(row=5, column=0, pady=5, sticky="w")
    global quantity_var
    quantity_var = tk.IntVar(purchase_window, value=1)
    quantity_spinbox = tk.Spinbox(input_frame, from_=1, to=100, textvariable=quantity_var, width=10)
    quantity_spinbox.grid(row=5, column=1, pady=5, sticky="w")

    # Total
    tk.Label(input_frame, text="Total:").grid(row=6, column=0, pady=5, sticky="w")
    global total_entry
    total_entry = tk.Entry(input_frame, state='readonly', width=30)
    total_entry.grid(row=6, column=1, pady=5)

    # Payment Method
    tk.Label(input_frame, text="Payment Method:").grid(row=7, column=0, pady=5, sticky="w")
    payment_method_var = tk.StringVar(purchase_window)
    payment_method_dropdown = tk.OptionMenu(input_frame, payment_method_var, "Cash", "UPI", "Card")
    payment_method_var.set("Cash")  # Default
    payment_method_dropdown.grid(row=7, column=1, pady=5, sticky="w")

    # Fetch product prices once
    product_prices = fetch_product_prices()

    # Update amount based on selected product's price
    def update_amount():
        selected_product = product_name_var.get()
        amount = product_prices.get(selected_product, 0)
        amount_entry.config(state='normal')
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, str(amount))
        amount_entry.config(state='readonly')
        update_total()

    # Update total based on quantity and amount
    def update_total():
        try:
            amount = float(amount_entry.get())
            quantity = quantity_var.get()
            total = round(amount * quantity, 2)  # Rounded to 2 decimal places
            total_entry.config(state='normal')
            total_entry.delete(0, tk.END)
            total_entry.insert(0, str(total))
            total_entry.config(state='readonly')
        except ValueError:
            pass

    # Update amount and total when product or quantity changes
    product_name_var.trace_add("write", lambda *args: update_amount())
    quantity_var.trace_add("write", lambda *args: update_total())

    # Place order button
    tk.Button(purchase_window, text="Place Order", command=lambda: place_order(
        customer_name_entry.get(), contact_number_entry.get(),
        product_name_var.get(), quantity_var.get(), payment_method_var.get()
    )).pack(pady=20)

# Function to validate and place order
def place_order(customer_name, contact_number, product_name, quantity, payment_method):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="furniture"
        )
        mycursor = mydb.cursor()

        # Fetch Customer_ID using customer_name and contact_number
        mycursor.execute("""
            SELECT Customer_ID FROM customer WHERE Customer_Name = %s AND Customer_PhNo = %s
        """, (customer_name, contact_number))
        customer_result = mycursor.fetchone()
        if not customer_result:
            messagebox.showerror("Error", "Customer not found. Please register the customer first.")
            return
        customer_id = customer_result[0]

        # Fetch Product_ID and Price
        mycursor.execute("SELECT Prod_ID, Prod_Price FROM product WHERE Prod_Name = %s", (product_name,))
        product_result = mycursor.fetchone()
        if not product_result:
            messagebox.showerror("Error", "Product not found.")
            return
        product_id, price = product_result

        # Calculate Total
        total = round(price * quantity, 2)

        # Insert data into purchase table
        mycursor.execute("""
            INSERT INTO purchase (Customer_ID, Product_ID, Quantity, Total, Payment_Method) 
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, product_id, quantity, total, payment_method))
        mydb.commit()

        messagebox.showinfo("Success", "Purchase order placed successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        mycursor.close()
        mydb.close()

# Function to display recent purchase based on order ID

def display_recent_purchase():
    """Create a new window for displaying recent purchase details."""
    recent_purchase_window = tk.Toplevel(root)
    recent_purchase_window.title("Recent Purchase")

    # Create label and entry field for entering order ID
    order_id_label = tk.Label(recent_purchase_window, text="Enter Order ID:")
    order_id_label.pack(pady=5)
    order_id_entry = tk.Entry(recent_purchase_window)
    order_id_entry.pack(pady=5)

    # Create button to display purchase details based on order ID
    display_button = tk.Button(recent_purchase_window, text="Display", command=lambda: fetch_purchase_details(order_id_entry.get()))
    display_button.pack(pady=10)

def fetch_purchase_details(order_id):
    """Fetch purchase details and warranty information based on the order ID."""
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # SQL query to fetch purchase details and warranty information
        mycursor.execute("""
            SELECT p.Customer_ID, c.Customer_Name, c.Customer_PhNo, p.purchase_id, 
                   pr.Prod_Name, pr.Prod_Price, p.Quantity, p.Total, p.Payment_Method,
                   w.Warranty_Start_Date, w.Warranty_End_Date, w.Warranty_Terms
            FROM purchase p
            JOIN customer c ON p.Customer_ID = c.Customer_ID
            JOIN product pr ON p.Product_ID = pr.Prod_ID
            LEFT JOIN warranty w ON p.purchase_id = w.Purchase_ID
            WHERE p.purchase_id = %s
        """, (order_id,))

        purchase_details = mycursor.fetchone()

        # Check if purchase details were found
        if purchase_details:
            # Extracting the details from the fetched data
            customer_id = purchase_details[0]
            customer_name = purchase_details[1]
            customer_phone = purchase_details[2]
            order_id = purchase_details[3]
            product_name = purchase_details[4]
            product_price = purchase_details[5]
            quantity = purchase_details[6]
            total = purchase_details[7]
            payment_method = purchase_details[8]
            warranty_start = purchase_details[9]
            warranty_end = purchase_details[10]
            warranty_terms = purchase_details[11]

            # Display the purchase details including warranty information
            messagebox.showinfo("Purchase Details", 
                f"Customer ID: {customer_id}\n"
                f"Customer Name: {customer_name}\n"
                f"Contact Number: {customer_phone}\n"
                f"Order ID: {order_id}\n"
                f"Product Name: {product_name}\n"
                f"Amount: {product_price}\n"
                f"Quantity: {quantity}\n"
                f"Total: {total}\n"
                f"Payment Method: {payment_method}\n"
                f"Warranty Start Date: {warranty_start}\n"
                f"Warranty End Date: {warranty_end}\n"
                f"Warranty Terms: {warranty_terms}"
            )
        else:
            messagebox.showwarning("Not Found", "No purchase found for the given Order ID.")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch purchase details: {err}")


# Function to display customer details based on customer ID
def display_customer_details():
    # Create a new window for displaying customer details
    customer_window = tk.Toplevel(root)
    customer_window.title("Customer Details")

    # Create label and entry field for entering customer ID
    customer_id_label = tk.Label(customer_window, text="Enter Customer ID:")
    customer_id_label.pack(pady=5)
    customer_id_entry = tk.Entry(customer_window)
    customer_id_entry.pack(pady=5)

    # Create button to display customer details based on customer ID
    display_button = tk.Button(customer_window, text="Display", command=lambda: fetch_customer_details(customer_id_entry.get()))
    display_button.pack(pady=10)

def fetch_customer_details(customer_id):
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute SQL query to fetch customer details based on customer ID
        mycursor.execute("SELECT customer_id, customer_name, customer_email, customer_Phno, Customer_Address FROM customer WHERE customer_id = %s", (customer_id,))
        customer_details = mycursor.fetchone()

        # Display customer details
        messagebox.showinfo("Customer Details", f"Customer ID: {customer_details[0]}\nCustomer Name: {customer_details[1]}\nEmail: {customer_details[2]}\nPhone Number: {customer_details[3]}\nAddress: {customer_details[4]}")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch customer details: {err}")

# Function to display offers based on offer type
def display_offers():
    # Create a new window for displaying offers
    offer_window = tk.Toplevel(root)
    offer_window.title("Offers")

    # Create label and dropdown menu for selecting offer type
    offer_type_label = tk.Label(offer_window, text="Select Offer Type:")
    offer_type_label.pack(pady=5)

    offer_type_var = tk.StringVar(offer_window)
    offer_type_var.set("Daily")  # Default offer type

    offer_type_options = ["Daily", "Weekend", "Holiday", "Monthly", "Clearance", "Festivals", "Yearly"]
    offer_type_dropdown = tk.OptionMenu(offer_window, offer_type_var, *offer_type_options)
    offer_type_dropdown.pack(pady=5)

    # Create button to display offers based on selected offer type
    display_button = tk.Button(offer_window, text="Display", command=lambda: fetch_offers(offer_type_var.get()))
    display_button.pack(pady=10)

def fetch_offers(offer_type):
    try:
        # Establish connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",  # Replace with your MySQL password
            database="furniture"
        )

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute SQL query to fetch offers based on selected offer type
        mycursor.execute("SELECT offer_id, offer_type, discount_percentage, product_included, Offer_Start_Date, Offer_End_Date FROM offer WHERE offer_type = %s", (offer_type,))
        offers = mycursor.fetchall()

        # Display offers
        offer_details = ""
        for offer in offers:
            offer_details += f"Offer ID: {offer[0]}\nOffer Type: {offer[1]}\nDiscount Percentage: {offer[2]}\nProduct Included: {offer[3]}\nOffer Start Date: {offer[4]}\nOffer End Date: {offer[5]}\n\n"

        messagebox.showinfo("Offers", offer_details)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        # Display error message if query fails
        messagebox.showerror("Error", f"Failed to fetch offers: {err}")

# Function to submit feedback
def submit_feedback():
    # Create a new window for submitting feedback
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Submit Feedback")

    # Create labels and entry fields for feedback details
    order_id_label = tk.Label(feedback_window, text="Order ID:")
    order_id_label.pack(pady=5)
    order_id_entry = tk.Entry(feedback_window)
    order_id_entry.pack(pady=5)

    rating_label = tk.Label(feedback_window, text="Rating (1-5):")
    rating_label.pack(pady=5)
    rating_var = tk.IntVar(feedback_window)
    rating_entry = tk.Spinbox(feedback_window, from_=1, to=5, textvariable=rating_var)
    rating_entry.pack(pady=5)

    text_feedback_label = tk.Label(feedback_window, text="Text Feedback:")
    text_feedback_label.pack(pady=5)
    text_feedback_entry = tk.Text(feedback_window, height=5, width=50)
    text_feedback_entry.pack(pady=5)

    # Function to submit feedback to the database
    def submit_feedback_to_database():
        try:
            # Establish connection to the database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",  # Replace with your MySQL password
                database="furniture"
            )

            # Create a cursor object to execute SQL queries
            mycursor = mydb.cursor()

            # Get feedback details from entry fields
            order_id = order_id_entry.get()
            rating = rating_var.get()
            text_feedback = text_feedback_entry.get("1.0", tk.END)

            # Execute SQL query to insert feedback into the database
            sql = "INSERT INTO feedback (order_id, rating, text_feedback) VALUES (%s, %s, %s)"
            val = (order_id, rating, text_feedback)
            mycursor.execute(sql, val)
            mydb.commit()

            # Display success message
            messagebox.showinfo("Success", "Feedback submitted successfully!")

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

        except mysql.connector.Error as err:
            # Display error message if query fails
            messagebox.showerror("Error", f"Failed to submit feedback: {err}")

    # Create button to submit feedback
    submit_button = tk.Button(feedback_window, text="Submit", command=submit_feedback_to_database)
    submit_button.pack(pady=10)

# Create the main application window
root.title("Furniture Store Management System")
root.geometry("650x600")
root.configure(bg='sky blue')  # Set background color to sky blue

welcome_label = tk.Label(root, text="Welcome to Furniture Store", font=FONT_TITLE, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
welcome_label.pack(pady=10)
# Create labels and entry fields for MySQL database credentials
username_label = tk.Label(root, text="Username:")

username_entry = tk.Entry(root)


password_label = tk.Label(root, text="Password:")

password_entry = tk.Entry(root, show="*")

# Create button to connect to the database
connect_button = tk.Button(root, text="Connect", command=connect_to_database)

# Style the username and password labels and entries
username_label.config(font=FONT_MAIN, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
password_label.config(font=FONT_MAIN, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
username_entry.config(font=FONT_MAIN, bg="white", fg=TEXT_COLOR)
password_entry.config(font=FONT_MAIN, bg="white", fg=TEXT_COLOR)
connect_button.config(font=FONT_MAIN, bg=PRIMARY_COLOR, fg="white", activebackground=SECONDARY_COLOR, relief="flat")

# For labels and buttons, add consistent padding
username_label.pack(pady=5)
username_entry.pack(pady=5)
password_label.pack(pady=5)
password_entry.pack(pady=5)
connect_button.pack(pady=10)

root.mainloop()
