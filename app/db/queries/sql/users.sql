-- name: get-user-by-email^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       created_at,
       updated_at,
       is_active
FROM "public"."user"
WHERE email = :email
LIMIT 1;


-- name: get-user-by-username^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       created_at,
       updated_at,
       is_active
FROM "public"."user"
WHERE username = :username
LIMIT 1;


-- name: create-new-user<!
INSERT INTO "public"."user" (username, email, salt, created_at, updated_at, hashed_password, is_active)
VALUES (:username, :email, :salt, :created_at, :updated_at, :hashed_password, :is_active)
RETURNING id, created_at, updated_at