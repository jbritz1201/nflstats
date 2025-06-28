select season, 
  rusher_player_id, 
  rusher_player_name,
  rb_name, 
  COALESCE(COUNT(DISTINCT old_game_id), 0) AS games,
  COALESCE(sum(rush_attempt),0) as RATT,
  COALESCE(sum(yards_gained),0) as RYDS, 
  COALESCE(sum(fumble),0) as FUM, 
  COALESCE(sum(fumble_lost),0) as FUMLOSS,
  COALESCE(sum(touchdown),0) RTDS,
  COALESCE(sum(first_down_rush),0) R1st,
  COALESCE(sum(sack),0) SACKS
  from 
  (select season, 
  TRIM(rusher_player_name) AS rusher_player_name,
  SPLIT_PART(TRIM(rusher_player_name), '.', 1) AS rusher_player_first_name,
  SPLIT_PART(TRIM(rusher_player_name), '.', 2) AS rusher_player_last_name,
  TRIM(rusher_player_last_name) || ',' || TRIM(rusher_player_first_name) AS rb_name,
  rusher_player_id, 
  rush_attempt,
  play_type, 
  yards_gained, 
  fumble, 
  fumble_lost, 
  touchdown, 
  first_down_rush, 
  sack,
  old_game_id
  from play_by_play 
  where play_type = 'run') group by season, rusher_player_id, rusher_player_name, rb_name
  order by season, sum(yards_gained) desc