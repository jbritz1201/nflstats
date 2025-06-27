SELECT 
    season, 
    ROUND(AVG(total_touchdowns)) as AVG_TD, 
    ROUND(AVG(total_interceptions)) as AVG_INT,
    ROUND(AVG(total_attempts)) as AVG_ATTEMPTS,
    ROUND(AVG(total_yards)) as AVG_YARDS,
    ROUND(AVG(total_completions)) as AVG_COMPLETIONS
FROM 
(
    SELECT
        season,
        passer_player_id,
        passer_player_name,
        SUM(passing_yards) AS total_yards,
        SUM(touchdown) AS total_touchdowns,
        SUM(interception) AS total_interceptions, 
        SUM(pass_attempt) AS total_attempts,
        SUM(complete_pass) AS total_completions
    FROM play_by_play
    WHERE passer_player_id IS NOT NULL
    GROUP BY season, passer_player_id, passer_player_name
    HAVING SUM(pass_attempt) >= 244
    ORDER BY season, passer_player_name
) AS qualified_by_attempts
WHERE season = ?
GROUP BY season