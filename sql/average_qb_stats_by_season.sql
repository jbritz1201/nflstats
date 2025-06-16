SELECT
    season,
    AVG(touchdowns) AS avg_touchdowns,
    AVG(interceptions) AS avg_interceptions
FROM qb_stats where games > 11
GROUP BY season
ORDER BY season