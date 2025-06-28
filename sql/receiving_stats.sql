select season, 
  receiver_player_id, 
  receiver_player_name,
  rec_name,
  COALESCE(COUNT(DISTINCT old_game_id), 0) AS games,
  COALESCE(sum(receiving_yards),0) as RECYDS,
  COALESCE (sum(complete_pass),0) as REC,
  COALESCE (sum(complete_pass) + sum(incomplete_pass),0) as TARG,
  COALESCE (sum(pass_touchdown),0) as RECTDS,
  COALESCE (sum(first_down_pass),0) as REC1STDS
  from 
  (select season, 
  TRIM(receiver_player_name) AS receiver_player_name,
  SPLIT_PART(TRIM(receiver_player_name), '.', 1) AS receiver_player_first_name,
  SPLIT_PART(TRIM(receiver_player_name), '.', 2) AS receiver_player_last_name,
  TRIM(receiver_player_last_name) || ',' || TRIM(receiver_player_first_name) AS rec_name,
  receiver_player_id, 
  receiving_yards,
  complete_pass,
  incomplete_pass,
  pass_touchdown,
  first_down_pass,
  play_type,
  old_game_id
  from play_by_play 
  where play_type = 'pass') group by season, receiver_player_id, receiver_player_name, rec_name
