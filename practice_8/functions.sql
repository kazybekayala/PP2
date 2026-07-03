--function to search contacts by username or phone
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(username VARCHAR, phone VARCHAR)
AS $$
BEGIN

    RETURN QUERY
    SELECT
        p.username,
        p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';

END;
$$ LANGUAGE plpgsql;

--function to display contacts with pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN

    RETURN QUERY
    SELECT
        phonebook.id,
        phonebook.username,
        phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT p_limit
    OFFSET p_offset;

END;
$$ LANGUAGE plpgsql;