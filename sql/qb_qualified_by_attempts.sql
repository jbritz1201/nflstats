SELECT
    season,
    passer_player_id,
    passer_player_name,
    SUM(pass_attempt) AS total_attempts
FROM play_by_play
WHERE passer_player_id IS NOT NULL
GROUP BY season, passer_player_id, passer_player_name
HAVING SUM(pass_attempt) >= ?
ORDER BY season, passer_player_name