SELECT *
FROM passer_stats
WHERE LOWER(qb_name) LIKE LOWER(?)
ORDER BY season