import axelrod as axl

axl.seed(0)  # Set a seed
players = [s() for s in axl.demo_strategies]  # Create players
tournament = axl.Tournament(players)  # Create a tournament
results = tournament.play()  # Play the tournament

print(results.ranked_names)  # Print the results of the tournament
