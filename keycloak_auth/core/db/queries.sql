-- name: create_tables
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id TEXT REFERENCES users(id),
    role TEXT NOT NULL,
    PRIMARY KEY (user_id, role)
);

-- name: upsert_user
INSERT OR REPLACE INTO users (id, username, email)
VALUES (:id, :username, :email);

-- name: set_roles
INSERT OR REPLACE INTO user_roles (user_id, role)
VALUES (:user_id, :role);

-- name: get_roles
SELECT role FROM user_roles WHERE user_id = :user_id;