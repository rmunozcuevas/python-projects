from nba_api.stats.endpoints import playercareerstats

# Anthony Davis
career = playercareerstats.PlayerCareerStats(player_id="203076")
career.get_data_frames()[0]