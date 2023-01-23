--name: get-message-by-id^
SELECT msg.id,
       msg.user_id,
       msg.status_code,
       msg.user_id as author_id,
       msg.created_at,
       msg.updated_at,
       msg.content,
       status.name as status_name,
       status.description as status_description,
       (SELECT ARRAY(
                SELECT number
                FROM "public"."messageNumbers" nums
                WHERE nums.message_id = msg.id
            )
       ) as numbers_arr
FROM "public"."message" msg
    INNER JOIN "public"."status" status ON status.code = msg.status_code
WHERE msg.id = :message_id

--name: get-user-messages
SELECT msg.id,
       msg.user_id,
       msg.status_code,
       msg.user_id as author_id,
       msg.created_at,
       msg.updated_at,
       msg.content,
       status.name as status_name,
       status.description as status_description,
       (SELECT ARRAY(
                SELECT number
                FROM "public"."messageNumbers" nums
                WHERE nums.message_id = msg.id
	        )
       ) as numbers_arr
FROM "public"."message" msg
    INNER JOIN "public"."status" status ON status.code = msg.status_code
WHERE msg.user_id = 1 AND msg.status_code <= 140
ORDER BY msg.created_at DESC
LIMIT 5000;

--name: get-message-numbers
SELECT number.id,
       number.number,
       number.message_id
FROM "public"."messageNumbers" number
WHERE number.message_id = :message_id

--name: create-message<!
INSERT INTO "public"."message" (content, user_id, created_at, updated_at, status_code)
VALUES (:content, :user_id, :created_at, :updated_at, :status_code)
RETURNING id, updated_at

--name: create-message-number<!
INSERT INTO "public"."messageNumbers" (number, message_id)
VALUES (:number, :message_id)
RETURNING id, number, message_id

--name: update-status-code<!
UPDATE "public"."message"
SET status_code = :status_code,
    updated_at = :updated_at
WHERE id = :message_id
RETURNING id, updated_at