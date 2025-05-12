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
VALUES ('ptthappy', 'Luiss-MacBook-Pro.local', 'Darwin', 'Darwin Kernel Version 24.3.0: Thu Jan  2 20:24:06 PST 2025; root:xnu-11215.81.4~3/RELEASE_ARM64_T8103')
ON CONFLICT DO NOTHING;