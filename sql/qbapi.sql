SELECT *
FROM qb_stats
WHERE LOWER(passer_player_name) LIKE LOWER(?)
ORDER BY season