SELECT
    passer_player_id,
    passer_player_name,
    season,
    SUM(pass_attempt) AS attempts,
    SUM(CASE WHEN complete_pass = 1 THEN 1 ELSE 0 END) AS completions,
    SUM(pass_touchdown) AS touchdowns,
    SUM(interception) AS interceptions,
    SUM(passing_yards) AS yards,
    SUM(fumble_lost) AS fumbles_lost,
    SUM(sack) AS sacks,
    SUM(first_down_pass) AS first_downs,
    COUNT(DISTINCT old_game_id) AS games
FROM play_by_play
WHERE passer_player_id IS NOT NULL AND passer_player_name IS NOT NULL
GROUP BY season, passer_player_id, passer_player_name
ORDER BY season, passer_player_id, passer_player_name