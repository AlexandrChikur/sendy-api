-- name: get-status-by-id^
SELECT status.id,
       status.code as status_code,
       status.name as status_code_name,
       status.description as status_code_description,
       header.id as status_header_id,
       header.name as status_header_name,
       header.description as status_header_description
FROM "public"."status" status
	INNER JOIN "public"."statusHeader" header ON status.status_header_id = header.id
WHERE status.id = :status_id
LIMIT 1;

-- name: get-statuses-by-header-id
SELECT status.id,
       status.code as status_code,
       status.name as status_code_name,
       status.description as status_code_description,
       header.id as status_header_id,
       header.name as status_header_name,
       header.description as status_header_description
FROM "public"."status" status
	INNER JOIN "public"."statusHeader" header ON status.status_header_id = header.id
WHERE header.id = :header_id
ORDER BY status.code