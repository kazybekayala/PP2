--create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--create groups table
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

--add foreign key
ALTER TABLE contacts
ADD CONSTRAINT fk_group
FOREIGN KEY (group_id)
REFERENCES groups(id);

--create phones table
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10)
        CHECK (type IN ('home', 'work', 'mobile')),
    FOREIGN KEY (contact_id)
    REFERENCES contacts(id)
    ON DELETE CASCADE
);

--insert default groups
INSERT INTO groups(name)
VALUES
('Family'),
('Friend'),
('Work'),
('Other')
ON CONFLICT (name) DO NOTHING;