CREATE SCHEMA IF NOT EXISTS machine;

CREATE TABLE IF NOT EXISTS machine.reg_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    hostname TEXT NOT NULL,
    os_name TEXT NOT NULL,
    os_version TEXT NOT NULL,
    registered_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (username, hostname)
);


INSERT INTO machine.reg_user (username, hostname, os_name, os_version)
VALUES ('{username}', '{hostname}', '{os_name}', '{os_version}')
ON CONFLICT DO NOTHING;
