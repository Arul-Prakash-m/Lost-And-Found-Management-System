import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import date

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PrakasH@2182K6",
        database="LostFoundDB"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print("Database connection error:", err)
    exit()

root = tk.Tk()
root.title("Lost & Found Management System")
root.geometry("920x670")
root.configure(bg="#1e2a38")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#ffffff")
style.configure("TLabel", font=("Segoe UI", 10), background="#ffffff", foreground="#2e2e2e")
style.configure("TButton", font=("Segoe UI", 10), background="#d4af37", foreground="#2e2e2e")
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("Treeview", rowheight=28, font=("Segoe UI", 10), background="white", fieldbackground="white")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#1e2a38", foreground="white")
style.map("TButton",
          background=[('active', '#f0cc6f')],
          foreground=[('pressed', 'black'), ('active', '#1e2a38')])

def submit_item():
    item_name = entry_name.get()
    desc = entry_desc.get("1.0", tk.END).strip()
    loc = entry_loc.get()
    status = status_var.get()
    if not item_name or not desc or not loc or not status:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return
    sql = "INSERT INTO items (item_name, description, date_reported, location_found, status) VALUES (%s, %s, %s, %s, %s)"
    val = (item_name, desc, date.today(), loc, status)
    cursor.execute(sql, val)
    db.commit()
    messagebox.showinfo("Success", f"{status} item reported successfully!")
    clear_form()
    view_items()

def view_items():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM items ORDER BY date_reported DESC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def search_items():
    keyword = entry_search.get()
    query = "SELECT * FROM items WHERE item_name LIKE %s OR description LIKE %s"
    val = (f'%{keyword}%', f'%{keyword}%')
    cursor.execute(query, val)
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def delete_item():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select an item", "Please select an item to delete.")
        return
    values = tree.item(selected, 'values')
    item_id = values[0]
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.commit()
    messagebox.showinfo("Deleted", "Item deleted successfully.")
    view_items()

def clear_form():
    entry_name.delete(0, tk.END)
    entry_desc.delete("1.0", tk.END)
    entry_loc.delete(0, tk.END)
    status_var.set("Lost")

entry_frame = ttk.LabelFrame(root, text="  Report Lost or Found Item", padding=15, style="TFrame")
entry_frame.pack(fill="x", padx=20, pady=10)

ttk.Label(entry_frame, text="Item Name:").grid(row=0, column=0, sticky="e", pady=5)
entry_name = ttk.Entry(entry_frame, width=40)
entry_name.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(entry_frame, text="Description:").grid(row=1, column=0, sticky="ne", pady=5)
entry_desc = tk.Text(entry_frame, width=38, height=3, font=("Segoe UI", 10), wrap="word")
entry_desc.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(entry_frame, text="Location:").grid(row=2, column=0, sticky="e", pady=5)
entry_loc = ttk.Entry(entry_frame, width=40)
entry_loc.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(entry_frame, text="Status:").grid(row=3, column=0, sticky="e", pady=5)
status_var = tk.StringVar(value="Lost")
status_menu = ttk.Combobox(entry_frame, textvariable=status_var, values=["Lost", "Found"], state="readonly", width=38)
status_menu.grid(row=3, column=1, padx=10, pady=5)

ttk.Button(entry_frame, text="Submit", command=submit_item).grid(row=4, columnspan=2, pady=15)

search_frame = ttk.LabelFrame(root, text="  Search Items", padding=15, style="TFrame")
search_frame.pack(fill="x", padx=20, pady=5)

entry_search = ttk.Entry(search_frame, width=60)
entry_search.pack(side="left", padx=(5, 10))
ttk.Button(search_frame, text="Search", command=search_items).pack(side="left")

tree_frame = ttk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

cols = ("ID", "Item Name", "Description", "Date", "Location", "Status")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor="center")

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

ttk.Button(root, text="Delete Selected", command=delete_item).pack(pady=10)

view_items()
root.mainloop()


