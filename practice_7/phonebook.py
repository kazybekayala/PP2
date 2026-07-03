import csv #module for working with CSV files
import psycopg2 #module for connecting Python to PostgreSQL
from config import load_config

#function to connect to the database
def connect_db():
    config = load_config() #read parameters from database.ini
    return psycopg2.connect(**config)

#import contacts from CSV file into PostgreSQL
def import_csv(filename):
    conn = connect_db()
    cur = conn.cursor()

    #open CSV file
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        #insert each row into the table
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (row["username"], row["phone"])
            )

    conn.commit() #save changes
    cur.close() #close cursor
    conn.close() #close connection
    print("Contacts imported successfully.")

#add a new contact from the keyboard
def insert_contact():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (username, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")

#show all contacts from the database
def show_contacts():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print("\nPhoneBook:")

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#search contact by username
def search_name():
    username = input("Enter username: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username = %s",
        (username,)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Contact not found.")

    cur.close()
    conn.close()

#search contacts by phone prefix
def search_prefix():
    prefix = input("Enter phone prefix: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

#update username or phone number
def update_contact():
    username = input("Enter current username: ")
    print("1 - Update username")
    print("2 - Update phone")
    choice = input("Choose: ")
    conn = connect_db()
    cur = conn.cursor()

    if choice == "1":
        new_name = input("Enter new username: ")

        cur.execute(
            "UPDATE phonebook SET username=%s WHERE username=%s",
            (new_name, username)
        )

    elif choice == "2":
        new_phone = input("Enter new phone: ")

        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE username=%s",
            (new_phone, username)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")

#delete contact by username or phone
def delete_contact():
    print("1 - Delete by username")
    print("2 - Delete by phone")
    choice = input("Choose: ")
    conn = connect_db()
    cur = conn.cursor()

    if choice == "1":
        username = input("Enter username: ")

        cur.execute(
            "DELETE FROM phonebook WHERE username=%s",
            (username,)
        )

    elif choice == "2":
        phone = input("Enter phone: ")

        cur.execute(
            "DELETE FROM phonebook WHERE phone=%s",
            (phone,)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")

#main menu
while True:
    print("\n========== PhoneBook ==========")
    print("1. Import contacts from CSV")
    print("2. Add new contact")
    print("3. Show all contacts")
    print("4. Search by username")
    print("5. Search by phone prefix")
    print("6. Update contact")
    print("7. Delete contact")
    print("0. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        import_csv("contacts.csv")

    elif choice == "2":
        insert_contact()

    elif choice == "3":
        show_contacts()

    elif choice == "4":
        search_name()

    elif choice == "5":
        search_prefix()

    elif choice == "6":
        update_contact()

    elif choice == "7":
        delete_contact()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")