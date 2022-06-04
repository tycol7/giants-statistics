# Tyler Coleman 5/8/21
import pandas as pd
pd.options.mode.chained_assignment = None

play_by_play = pd.read_json('play_by_play.json')
play_by_play['pitcher_name'] = play_by_play['pitcher_first_name'] + ' ' + play_by_play['pitcher_last_name']
play_by_play['hitter_name'] = play_by_play['hitter_first_name'] + ' ' + play_by_play['hitter_last_name']

pd.set_option('display.max_rows', None)

# 1. Who are the top 10 hitters with the most extra base hits?
most_XBH = play_by_play[['hitter_id', 'hitter_name', 'hitter_team', 'event_result']]
most_XBH = most_XBH[most_XBH['event_result'].notnull()]
most_XBH = most_XBH[most_XBH['event_result'].str.contains('single|double|triple|home_run')]
most_XBH = pd.crosstab([most_XBH.hitter_id, most_XBH.hitter_name, most_XBH.hitter_team], most_XBH.event_result)
most_XBH['XBH'] = most_XBH.apply(lambda hitter: hitter.double + hitter.triple + hitter.home_run, axis = 1)
most_XBH = most_XBH.sort_values(['XBH', 'single'], ascending = [False, False])
most_XBH = most_XBH.reset_index()
most_XBH = most_XBH.drop(columns=['hitter_id'])
most_XBH = most_XBH.reindex(columns=['hitter_name', 'hitter_team', 'XBH', 'single', 'double', 'triple', 'home_run'])
most_XBH.head(10).to_csv('csv/1_extra_base_hits.csv', index = False)

# 2. What are the top 10 hardest pitches thrown?
hardest_pitches = play_by_play[['pitcher_id', 'pitcher_name', 'pitcher_team', 'pitch_release_velocity', 'pitch_type']]
hardest_pitches = hardest_pitches.drop(columns=['pitcher_id'])
hardest_pitches = hardest_pitches.reindex(columns=['pitcher_name', 'pitcher_team', 'pitch_release_velocity', 'pitch_type'])
hardest_pitches = hardest_pitches.sort_values('pitch_release_velocity', ascending = False)
hardest_pitches.head(10).to_csv('csv/2_hardest_pitches.csv', index = False)

# 3. What is the average four seam fastball velocity for each team's pitchers?
average_four_seam = play_by_play[['pitcher_team', 'pitch_release_velocity', 'pitch_type']]
average_four_seam = average_four_seam[average_four_seam.pitch_type == 'four_seam']
average_four_seam = average_four_seam.groupby('pitcher_team').agg({
    'pitch_release_velocity': 'mean'
})
average_four_seam.T.to_csv('csv/3_average_fastball.csv', index = False)

# 4. Who are the top 5 batting average leaders?
batting_leaders = play_by_play[['hitter_id', 'hitter_first_name', 'hitter_name', 'hitter_team', 'pitch_call', 'event_result', 'is_strikeout', 'is_base_on_balls']]
batting_leaders = batting_leaders[(batting_leaders.pitch_call == 'hit_by_pitch') | (batting_leaders.event_result.notnull()) | (batting_leaders.is_strikeout) | (batting_leaders.is_base_on_balls)]
plate_appearances = batting_leaders.groupby(['hitter_id', 'hitter_first_name' , 'hitter_name', 'hitter_team'], as_index = False).agg({
    'hitter_first_name': 'count'
})
plate_appearances.rename(columns = {'hitter_first_name' : 'plate_appearances'}, inplace = True)
at_bats = batting_leaders[(batting_leaders.event_result != 'sacrifice') & (~batting_leaders.is_base_on_balls) & (batting_leaders.pitch_call != 'hit_by_pitch')]
at_bats = at_bats.groupby(['hitter_id'], as_index = False).agg({
    'hitter_name': 'count'
})
at_bats.rename(columns = {'hitter_name' : 'at_bats'}, inplace = True)
hits = batting_leaders[batting_leaders.event_result.isin(['single', 'double', 'triple', 'home_run'])]
hits = hits.groupby(['hitter_id'], as_index = False).agg({
    'hitter_name': 'count'
})
hits.rename(columns = {'hitter_name' : 'hits'}, inplace = True)
batting_leaders = pd.merge(plate_appearances, at_bats, on = 'hitter_id')
batting_leaders = pd.merge(batting_leaders, hits, on = 'hitter_id')
batting_leaders['batting_average'] = batting_leaders.apply(lambda hitter: '%.3f'%(hitter.hits / hitter.at_bats), axis = 1)
batting_leaders = batting_leaders.sort_values('batting_average', ascending = False)
batting_leaders = batting_leaders.drop(columns=['hitter_id', 'at_bats'])
batting_leaders = batting_leaders.reindex(columns=['hitter_name', 'hitter_team', 'batting_average', 'hits', 'plate_appearances'])
batting_leaders.head(5).to_csv('csv/4_batting_averages.csv', index = False)

# 5. What is the OPS with runners in scoring position for each team?
ops_scoring_position = play_by_play[['hitter_team', 'runner_on_second_sfg_id', 'runner_on_third_sfg_id', 'pitch_call', 'event_result', 'is_strikeout', 'is_base_on_balls']]
ops_scoring_position = ops_scoring_position[(ops_scoring_position.runner_on_second_sfg_id.notnull()) | (ops_scoring_position.runner_on_third_sfg_id.notnull())]
ops_scoring_position = ops_scoring_position[(ops_scoring_position.event_result.notnull()) | (ops_scoring_position.is_strikeout) | (ops_scoring_position.is_base_on_balls) | (ops_scoring_position.pitch_call == 'hit_by_pitch')]
ops_scoring_position = ops_scoring_position.drop(columns=['runner_on_second_sfg_id', 'runner_on_third_sfg_id'])
walks_hbp = ops_scoring_position[(ops_scoring_position.is_base_on_balls) | (ops_scoring_position.pitch_call == 'hit_by_pitch')]
walks_hbp = walks_hbp.groupby(['hitter_team'], as_index = False).agg({
    'pitch_call': 'count'
})
walks_hbp.rename(columns = {'pitch_call' : 'walks_hbp'}, inplace = True)
at_bats = ops_scoring_position[(ops_scoring_position.event_result != 'sacrifice') & (~ops_scoring_position.is_base_on_balls) & (ops_scoring_position.pitch_call != 'hit_by_pitch')]
at_bats = at_bats.groupby(['hitter_team'], as_index = False).agg({
    'pitch_call': 'count'
})
at_bats.rename(columns = {'pitch_call': 'at_bats'}, inplace = True)
total_bases = ops_scoring_position[ops_scoring_position.event_result.isin(['single', 'double', 'triple', 'home_run'])]
hits = total_bases.groupby(['hitter_team'], as_index = False).agg({
    'pitch_call': 'count'
})
hits.rename(columns = {'pitch_call': 'hits'}, inplace = True)
def hit_value(hit):
    values = {'single': 1, 'double': 2, 'triple': 3, 'home_run': 4}
    return values[hit['event_result']]
total_bases['weight'] = total_bases.apply(hit_value, axis = 1)
total_bases = total_bases.groupby(['hitter_team', 'weight'], as_index = False).agg({
    'pitch_call': 'count'
})
total_bases.rename(columns = {'pitch_call': 'occurences'}, inplace = True)
total_bases['total_bases'] = total_bases.apply(lambda hit: hit.weight * hit.occurences, axis = 1)
total_bases = total_bases.groupby(['hitter_team'], as_index = False).agg({
    'total_bases': 'sum'
})
ops_scoring_position = pd.merge(walks_hbp, at_bats, on = 'hitter_team')
ops_scoring_position = pd.merge(ops_scoring_position, hits, on = 'hitter_team')
ops_scoring_position = pd.merge(ops_scoring_position, total_bases, on = 'hitter_team')
ops_scoring_position['OBP'] = ops_scoring_position.apply(lambda team: (team.hits + team.walks_hbp) / (team.at_bats + team.walks_hbp), axis = 1)
ops_scoring_position['SLG'] = ops_scoring_position.apply(lambda team: team.total_bases / team.at_bats, axis = 1)
ops_scoring_position['OPS'] = ops_scoring_position.apply(lambda team: team.OBP + team.SLG, axis = 1)
ops_scoring_position = ops_scoring_position[['hitter_team', 'OPS']]
ops_scoring_position.T.to_csv('csv/5_ops.csv', index = False, header = False)

# Bonus: List all the pitches thrown that have the exact same velocity
same_velocity = play_by_play[['pitcher_name', 'pitcher_team', 'pitch_release_velocity', 'pitch_type', 'inning', 'balls', 'strikes', 'outs']]
same_velocity = same_velocity[same_velocity['pitch_release_velocity'].notnull()]
same_velocity_query = same_velocity.groupby(['pitch_release_velocity'], as_index = False).agg({
    'pitcher_name': 'count'
})
same_velocity_query = same_velocity_query.query('pitcher_name>1')
same_velocity = same_velocity[same_velocity['pitch_release_velocity'].isin(same_velocity_query['pitch_release_velocity'])]
same_velocity.to_csv('csv/6_bonus.csv', index = False)
'''
The Big-O runtime to find pitches of the same velocity is O(n), where n is the number of pitches in play_by_play.json:

1. Iterate through all pitches, grouping by pitch velocity - O(n)
2. Select pitch velocities that occur more than once - O(n)
3. Iterate through all pitches, selecting pitch velocities found in step 2 - O(n)*

*Assuming pandas stores keys in a hashmap with O(1) lookup. If pandas stores keys in a list with O(m) lookup, where m is the same velocity pitches, the overall runtime would be O(n*m).
'''
