SELECT
match_id,
radiant_win,
radiant_team_id,
dire_team_id,
picks_bans
FROM matches
JOIN match_patch using(match_id)
JOIN leagues using(leagueid)
JOIN player_matches using(match_id)
JOIN heroes on heroes.id = player_matches.hero_id
LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
LEFT JOIN teams using(team_id)
WHERE TRUE
AND matches.leagueid = 15475
AND matches.start_time >= extract(epoch from timestamp '2023-07-05T16:00:51.067Z')
GROUP BY matches.match_id
HAVING count(distinct match_id) >= 1
ORDER BY matches.match_id
LIMIT 10000