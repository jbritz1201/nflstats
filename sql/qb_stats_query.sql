SELECT
    passer_player_id,
    passer_player_name,
    season,
    COALESCE(SUM(pass_attempt), 0) AS attempts,
    COALESCE(SUM(CASE WHEN complete_pass = 1 THEN 1 ELSE 0 END), 0) AS completions,
    COALESCE(SUM(pass_touchdown), 0) AS touchdowns,
    COALESCE(SUM(interception), 0) AS interceptions,
    COALESCE(SUM(passing_yards), 0) AS yards,
    COALESCE(SUM(fumble_lost), 0) AS fumbles_lost,
    COALESCE(SUM(sack), 0) AS sacks,
    COALESCE(SUM(first_down_pass), 0) AS first_downs,
    COALESCE(COUNT(DISTINCT old_game_id), 0) AS games
FROM play_by_play
WHERE passer_player_id IS NOT NULL AND passer_player_name IS NOT NULL
GROUP BY season, passer_player_id, passer_player_name
ORDER BY season, passer_player_id, passer_player_name