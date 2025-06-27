SELECT *
FROM qb_stats
WHERE LOWER(qb_name) LIKE LOWER(?)
ORDER BY season