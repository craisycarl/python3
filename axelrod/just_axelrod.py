import axelrod as axl

# The weights of the Prisoner's Dilemma outcomes. By default these are setup for you to be 3, 1, 0, 5.
print(axl.game.DefaultGame.RPST())

# The actions called 'A play' in axelrod
C = axl.Actions.C
D = axl.Actions.D

# These are NOT objects just a simple string of the letter 'C' or 'D'
print(C)
print(D)

# A turn looks like this
me, opponent = axl.Cooperator(), axl.TrickyCooperator()
me.play(opponent)

# Print my history from the turn. There's no score yet to see who won. I think that comes from a 'Match'.
print(me.history)

# Format the players for the match. The format must be a tuple.
# A little bit about the players. The Cooperator is simple, he just cooperates every turn. The TrickyCooperator is a
# little bit more complex. She almost always cooperates but will try and trick the opponent by defecting.
# After 3 rounds, if the opponent has not defected to a max history of 10, she defects.
players = (me, opponent)
# Create the match for 25 turns
match = axl.Match(players, turns=25)
# Now that it's all setup, run the match for the specified number of turns.
match.play()
# Okay finally let's get to some results of the match. It's nice that axelrod has some built in functions
# to view the data
# Here's a visual printout of what each player did. Again no score just some lines on the screen instead of 'C' and 'D'.
print(match.sparklines(c_symbol='|', d_symbol='-'))
print(match.sparklines())
# Great, now WHO WON?
print(match.scores())
# So that's who won for each play, but how about out of the 25 turns?
print(match.final_score())
# Nice. The Cooperator got smoked. 9 to 119! How about instead of raw score, the score per turn.
# The closer to 5 the better.
print(match.final_score_per_turn())
# Cool. But now how about you just tell me the winner. I don't care what the score was.
print(match.winner())
# Some extra stuff... Get the count of when both players cooperated.
print(match.cooperation())
# Some extra stuff... Get the normalized count of the cooperation. Just divide by the number of turns.
# If you always cooperated then your cooperation score would be 1.0.
print(match.normalised_cooperation())

# Okay, so far we have a good idea of what two players playing a match look like. But what about a bunch of players of
# all different strategies? That's what axelrod calls a tournament.

# So let's bring back our first two players and add three more
players = [me, opponent, axl.Defector(), axl.TitForTat(), axl.Random()]
# Fire up a tournament
tournament = axl.Tournament(players)
# Play it
results = tournament.play()
# So who won?
print(results.ranked_names)

# Fire up a tournament with some new players
players = [axl.DoubleCrosser(), axl.BackStabber(), axl.MetaHunter(), axl.FoolMeOnce(), axl.Grudger(),
           axl.MetaWinnerMemoryOne(), axl.NiceAverageCopier(), axl.MetaWinnerLongMemory(), axl.MetaWinner(),
           axl.MetaWinnerFiniteMemory(), axl.ForgetfulFoolMeOnce(), axl.TitForTat(), axl.Cooperator(), axl.Defector()
           ]
players = [s() for s in axl.ordinary_strategies]
tournament = axl.Tournament(players)
results = tournament.play(filename="basic_tournament.csv")
# So who won?
print(results.ranked_names)
print(results.normalised_scores)

# Now plot it
plot = axl.Plot(results)
plot.save_all_plots()
print('all done')
