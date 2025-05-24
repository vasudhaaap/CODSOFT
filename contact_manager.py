import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to database (or create if not exists)
conn = sqlite3.connect('contacts.db')
cur = conn.cursor()

# Create contacts table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
''')
conn.commit()

# Function to add a new contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showwarning("Warning", "Please enter both Name and Phone")
        return

    cur.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Contact added!")
    clear_fields()
    load_contacts()

# Function to clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    update_btn.config(state=tk.DISABLED)
    delete_btn.config(state=tk.DISABLED)

# Function to load all contacts into the listbox
def load_contacts():
    contact_list.delete(0, tk.END)
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        contact_list.insert(tk.END, f"{row[0]}: {row[1]} | {row[2]}")

# Function to search contacts by name or phone
def search_contacts():
    term = search_entry.get()
    contact_list.delete(0, tk.END)
    cur.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f'%{term}%', f'%{term}%'))
    rows = cur.fetchall()
    for row in rows:
        contact_list.insert(tk.END, f"{row[0]}: {row[1]} | {row[2]}")

# When user clicks a contact in the list, load details into fields
def on_select(event):
    try:
        index = contact_list.curselection()[0]
        selected = contact_list.get(index)
        contact_id = selected.split(":")[0]
        cur.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        row = cur.fetchone()

        name_entry.delete(0, tk.END)
        name_entry.insert(0, row[1])

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, row[2])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, row[3])

        address_entry.delete(0, tk.END)
        address_entry.insert(0, row[4])

        update_btn.config(state=tk.NORMAL)
        delete_btn.config(state=tk.NORMAL)
    except IndexError:
        pass  # Nothing selected

# Function to update selected contact
def update_contact():
    try:
        index = contact_list.curselection()[0]
        selected = contact_list.get(index)
        contact_id = selected.split(":")[0]

        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone can't be empty")
            return

        cur.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                    (name, phone, email, address, contact_id))
        conn.commit()
        messagebox.showinfo("Updated", "Contact updated!")
        clear_fields()
        load_contacts()
    except IndexError:
        messagebox.showerror("Error", "Please select a contact first")

# Function to delete selected contact
def delete_contact():
    try:
        index = contact_list.curselection()[0]
        selected = contact_list.get(index)
        contact_id = selected.split(":")[0]

        cur.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Contact deleted!")
        clear_fields()
        load_contacts()
    except IndexError:
        messagebox.showerror("Error", "Please select a contact first")

# Set up the main window
root = tk.Tk()
root.title("Simple Contact Manager")

# Set background color to red
root.configure(bg='red')

# Labels and entries with white text on red bg for readability
label_fg = 'white'
entry_bg = 'white'

tk.Label(root, text="Name", bg='red', fg=label_fg).grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root, bg=entry_bg)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Phone", bg='red', fg=label_fg).grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(root, bg=entry_bg)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email", bg='red', fg=label_fg).grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(root, bg=entry_bg)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Address", bg='red', fg=label_fg).grid(row=3, column=0, padx=5, pady=5)
address_entry = tk.Entry(root, bg=entry_bg)
address_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons (keep default bg for contrast)
tk.Button(root, text="Add Contact", command=add_contact).grid(row=4, column=0, pady=10)
update_btn = tk.Button(root, text="Update Contact", command=update_contact, state=tk.DISABLED)
update_btn.grid(row=4, column=1)
delete_btn = tk.Button(root, text="Delete Contact", command=delete_contact, state=tk.DISABLED)
delete_btn.grid(row=4, column=2)

# Search label and entry
tk.Label(root, text="Search", bg='red', fg=label_fg).grid(row=5, column=0, padx=5, pady=5)
search_entry = tk.Entry(root, bg=entry_bg)
search_entry.grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Search", command=search_contacts).grid(row=5, column=2)

# Listbox with scrollbar
contact_list = tk.Listbox(root, width=50)
contact_list.grid(row=6, column=0, columnspan=3, pady=10)
contact_list.bind('<<ListboxSelect>>', on_select)

# View all contacts button
tk.Button(root, text="View All Contacts", command=load_contacts).grid(row=7, column=0, columnspan=3)

# Load all contacts on start
load_contacts()

root.mainloop()
