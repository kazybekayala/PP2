--insert a new contact or update phone number
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE username = p_username
    ) THEN

        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;

    ELSE

        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);

    END IF;

END;
$$;

--insert multiple contacts (invalid phone numbers are skipped)
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN

    FOR i IN 1..array_length(p_names, 1)
    LOOP

        -- Check that phone contains exactly 11 digits
        IF p_phones[i] ~ '^[0-9]{11}$' THEN

            INSERT INTO phonebook(username, phone)
            VALUES (p_names[i], p_phones[i]);

        ELSE

            RAISE NOTICE
            'Invalid phone number: % (%).',
            p_names[i],
            p_phones[i];

        END IF;

    END LOOP;

END;
$$;

--delete contact by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM phonebook
    WHERE username = p_value
       OR phone = p_value;

END;
$$;