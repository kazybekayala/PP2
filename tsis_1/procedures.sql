--search contacts by username, email or phone
CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE(
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
AS $$
BEGIN

    RETURN QUERY

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

    WHERE

        c.username ILIKE '%' || p_query || '%'

        OR

        c.email ILIKE '%' || p_query || '%'

        OR

        p.phone ILIKE '%' || p_query || '%';

END;
$$ LANGUAGE plpgsql;

--add new phone number to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN

    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF v_contact_id IS NOT NULL THEN

        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_type);

    ELSE

        RAISE NOTICE 'Contact not found.';

    END IF;

END;
$$;

--move contact to another group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN

        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;

    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE username = p_contact_name;

END;
$$;

--function for pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    username VARCHAR,
    email VARCHAR,
    birthday DATE
)
AS $$
BEGIN

    RETURN QUERY

    SELECT
        c.username,
        c.email,
        c.birthday
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;

END;
$$ LANGUAGE plpgsql;