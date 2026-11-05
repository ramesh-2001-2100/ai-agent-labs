CREATE TABLE IF NOT EXISTS emails (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id   TEXT    NOT NULL UNIQUE,
    username   TEXT    NOT NULL,
    domain     TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_emails_domain ON emails(domain);

INSERT INTO emails (email_id, username, domain) VALUES
('john@gmail.com', 'john', 'gmail.com'),
('jane.smith@teachership.org', 'jane.smith', 'teachership.org'),
('alice.jones@saveplanet.net', 'alice.jones', 'saveplanet.net'),
('bob.wilson@gmail.com', 'bob.wilson', 'gmail.com'),
('charlie.brown@teachership.org', 'charlie.brown', 'teachership.org');

SELECT * FROM emails WHERE domain = 'gmail.com';

