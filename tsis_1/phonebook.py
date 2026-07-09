import csv
import json
import psycopg2
from config import load_config

#connect to PostgreSQL
def connect_db():
    config = load_config()
    return psycopg2.connect(**config)

#add new contact
def add_contact():
    username = input("Enter username: ")
    email = input("Enter email: ")
    birthday = input("Enter birthday (YYYY-MM-DD): ")
    group = input("Enter group: ")
    group = group.capitalize()
    phone = input("Enter phone: ")
    phone_type = input("Enter phone type (home/work/mobile): ").lower()
    conn = connect_db()
    cur = conn.cursor()

    #create group if it does not exist
    cur.execute(
        """
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT(name) DO NOTHING
        """,
        (group,)
    )
    cur.execute(
        "SELECT id FROM groups WHERE name=%s",
        (group,)
    )
    group_id = cur.fetchone()[0]
    cur.execute(
        """
        INSERT INTO contacts(username, email, birthday, group_id)
        VALUES(%s,%s,%s,%s)
        """,
        (username, email, birthday, group_id)
    )
    cur.execute(
        "SELECT id FROM contacts WHERE username=%s",
        (username,)
    )
    contact_id = cur.fetchone()[0]
    cur.execute(
        """
        INSERT INTO phones(contact_id, phone, type)
        VALUES(%s,%s,%s)
        """,
        (
        contact_id,
        phone,
        phone_type
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully.")

#add another phone number
def add_phone():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    phone_type = input("Enter type (home/work/mobile): ")
    phone_type = phone_type.lower()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "CALL add_phone(%s,%s,%s)",
        (username, phone, phone_type)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Phone added successfully.")

#search contacts by username, email or phone
def search_contacts():
    query = input("Enter search text: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )
    rows = cur.fetchall()
    if rows:
        print("\nSearch results:")
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()

#search contacts by email
def search_email():
    email = input("Enter email: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT username, email
        FROM contacts
        WHERE email ILIKE %s
        """,
        ("%" + email + "%",)
    )
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()

#filter contacts by group
def filter_group():
    group = input("Enter group: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.username, g.name
        FROM contacts c
        JOIN groups g
        ON c.group_id = g.id
        WHERE g.name ILIKE %s
        """,
        ("%" + group + "%",)
    )
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()

#sort contacts
def sort_contacts():
    print("1 - Sort by username")
    print("2 - Sort by birthday")
    print("3 - Sort by date added")
    choice = input("Choose: ")
    conn = connect_db()
    cur = conn.cursor()
    if choice == "1":
        cur.execute(
            """
            SELECT username, email, birthday
            FROM contacts
            ORDER BY username
            """
        )
    elif choice == "2":
        cur.execute(
            """
            SELECT username, email, birthday
            FROM contacts
            ORDER BY birthday
            """
        )
    elif choice == "3":
        cur.execute(
            """
            SELECT username, email, birthday
            FROM contacts
            ORDER BY created_at
            """
        )
    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

#export contacts to JSON
def export_json():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            c.username,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        """
    )
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({
            "username": row[0],
            "email": row[1],
            "birthday": str(row[2]),
            "group": row[3],
            "phone": row[4],
            "phone_type": row[5]
        })
    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    cur.close()
    conn.close()
    print("Contacts exported successfully.")

#import contacts from JSON
def import_json():
    with open("contacts.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    conn = connect_db()
    cur = conn.cursor()
    for contact in data:
        contact["group"] = contact["group"].capitalize()
        contact["phone_type"] = contact["phone_type"].lower()
        cur.execute(
            "SELECT id FROM contacts WHERE username=%s",
            (contact["username"],)
        )
        exists = cur.fetchone()
        if exists:
            answer = input(
                f"{contact['username']} already exists. "
                "Skip or overwrite? (s/o): "
            )
            if answer.lower() == "s":
                continue
            elif answer.lower() == "o":
                cur.execute(
                    """
                    INSERT INTO groups(name)
                    VALUES(%s)
                    ON CONFLICT(name) DO NOTHING
                    """,
                    (contact["group"],)
                )
                cur.execute(
                    "SELECT id FROM groups WHERE name=%s",
                    (contact["group"],)
                )
                group_id = cur.fetchone()[0]
                cur.execute(
                    """
                    UPDATE contacts
                    SET email=%s,
                    birthday=%s,
                    group_id=%s
                    WHERE username=%s
                    """,
                    (
                    contact["email"],
                    contact["birthday"],
                    group_id,
                    contact["username"]
                    )
                )
                cur.execute(
                    "SELECT id FROM contacts WHERE username=%s",
                    (contact["username"],)
                )
                contact_id = cur.fetchone()[0]

                cur.execute(
                    "DELETE FROM phones WHERE contact_id=%s",
                    (contact_id,)
                )
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s,%s,%s)
                    """,
                    (
                    contact_id,
                    contact["phone"],
                    contact["phone_type"]
                    )
                )
                continue
        cur.execute(
            """
            INSERT INTO groups(name)
            VALUES(%s)
            ON CONFLICT(name) DO NOTHING
            """,
            (contact["group"],)
        )
        cur.execute(
            "SELECT id FROM groups WHERE name=%s",
            (contact["group"],)
        )
        group_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO contacts(
                username,
                email,
                birthday,
                group_id
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                contact["username"],
                contact["email"],
                contact["birthday"],
                group_id
            )
        )
        cur.execute(
            "SELECT id FROM contacts WHERE username=%s",
            (contact["username"],)
        )
        contact_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO phones(
                contact_id,
                phone,
                type
            )
            VALUES(%s,%s,%s)
            """,
            (
                contact_id,
                contact["phone"],
                contact["phone_type"]
            )
        )
    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported successfully.")

#import contacts from CSV
def import_csv():
    conn = connect_db()
    cur = conn.cursor()
    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["group"] = row["group"].capitalize()
            row["phone_type"] = row["phone_type"].lower()
            cur.execute(
                """
                INSERT INTO groups(name)
                VALUES(%s)
                ON CONFLICT(name) DO NOTHING
                """,
                (row["group"],)
            )
            cur.execute(
                "SELECT id FROM groups WHERE name=%s",
                (row["group"],)
            )
            group_id = cur.fetchone()[0]
            cur.execute(
                "SELECT id FROM contacts WHERE username=%s",
                (row["username"],)
            )
            if cur.fetchone():
                continue
            cur.execute(
                """
                INSERT INTO contacts(
                    username,
                    email,
                    birthday,
                    group_id
                )
                VALUES(%s,%s,%s,%s)
                """,
                (
                    row["username"],
                    row["email"],
                    row["birthday"],
                    group_id
                )
            )
            cur.execute(
                "SELECT id FROM contacts WHERE username=%s",
                (row["username"],)
            )
            contact_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO phones(
                    contact_id,
                    phone,
                    type
                )
                VALUES(%s,%s,%s)
                """,
                (
                    contact_id,
                    row["phone"],
                    row["phone_type"]
                )
            )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported successfully.")

#show contacts with pagination
def pagination():
    limit = 3
    offset = 0
    while True:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s,%s)",
            (limit, offset)
        )
        rows = cur.fetchall()
        print("\n========== Contacts ==========")
        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
        cur.close()
        conn.close()
        print("\nnext - Next page")
        print("prev - Previous page")
        print("quit - Exit")
        choice = input("Choose: ").lower()
        if choice == "next":
            offset += limit
        elif choice == "prev":
            offset = max(0, offset - limit)
        elif choice == "quit":
            break
        else:
            print("Invalid choice.")

#move contact to another group
def move_group():
    username = input("Enter username: ")
    group = input("Enter new group: ")
    group = group.capitalize()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "CALL move_to_group(%s,%s)",
        (username, group)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact moved successfully.")

#main menu
while True:
    print("\n========== PhoneBook ==========")
    print("1. Add contact")
    print("2. Add phone")
    print("3. Search contacts")
    print("4. Search by email")
    print("5. Filter by group")
    print("6. Sort contacts")
    print("7. Export to JSON")
    print("8. Import from JSON")
    print("9. Import from CSV")
    print("10. Pagination")
    print("11. Move to another group")
    print("0. Exit")
    choice = input("Choose: ")
    if choice == "1":
        add_contact()
    elif choice == "2":
        add_phone()
    elif choice == "3":
        search_contacts()
    elif choice == "4":
        search_email()
    elif choice == "5":
        filter_group()
    elif choice == "6":
        sort_contacts()
    elif choice == "7":
        export_json()
    elif choice == "8":
        import_json()
    elif choice == "9":
        import_csv()
    elif choice == "10":
        pagination()
    elif choice == "11":
        move_group()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")