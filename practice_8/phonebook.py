import psycopg2
from config import load_config

#connect to PostgreSQL
def connect_db():
    config = load_config()
    return psycopg2.connect(**config)

#search contacts using PostgreSQL function
def search_contacts():
    pattern = input("Enter name or phone: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (pattern,)
    )

    rows = cur.fetchall()

    if rows:
        print("\nResults:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

#insert or update contact using stored procedure
def upsert_contact():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "CALL upsert_contact(%s,%s)",
        (username, phone)
    )

    conn.commit()
    print("Operation completed.")
    cur.close()
    conn.close()

#insert multiple contacts using stored procedure
def insert_many_contacts():
    n = int(input("How many contacts to add? "))

    names = []
    phones = []

    for i in range(n):
        print(f"\nContact {i+1}")
        names.append(input("Username: "))
        phones.append(input("Phone: "))

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_contacts(%s, %s)",
        (names, phones)
    )

    conn.commit()
    print("Contacts processed.")

    cur.close()
    conn.close()

#show contacts with pagination
def show_paginated():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s,%s)",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#delete contact using stored procedure
def delete_contact():
    value = input("Enter username or phone: ")
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "CALL delete_contact(%s)",
        (value,)
    )

    conn.commit()
    print("Contact deleted.")
    cur.close()
    conn.close()

#main menu
while True:
    print("\n===== PhoneBook =====")
    print("1. Search contacts")
    print("2. Insert / Update contact")
    print("3. Insert multiple contacts")
    print("4. Show contacts (pagination)")
    print("5. Delete contact")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        search_contacts()

    elif choice == "2":
        upsert_contact()

    elif choice == "3":
        insert_many_contacts()

    elif choice == "4":
        show_paginated()

    elif choice == "5":
        delete_contact()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")