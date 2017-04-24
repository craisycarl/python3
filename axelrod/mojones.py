from axelrod.actions import Actions  # Action
from axelrod.player import Player
import axelrod

C, D = Actions.C, Actions.D


class LookerUp(Player):

    def __init__(self, lookup_table):
        self.lookup_table = lookup_table

    def strategy(self, opponent):
        # If there isn't enough history to lookup an action, cooperate.
        if len(self.history) < 2:
            return C

        # Get my own lat two actions
        my_history = ''.join(self.history[-2:])

        # Do the same for the opponent.
        opponent_history = ''.join(opponent.history[-2:])

        # Get the opponents first two actions.
        opponent_start = ''.join(opponent.history[:2])

        # Put these three strings together in a tuple.
        key = (opponent_start, my_history, opponent_history)

        # Look up the action associated with that tuple in the lookup table.
        action = self.lookup_table[key]

        return action

# this table actually has all 64 possible keys
cooperator_table = {
    ('CC', 'CC', 'CC'): 'C',
    ('CC', 'CC', 'CD'): 'C',
    ('CC', 'CC', 'DC'): 'C',
    ('CC', 'CC', 'DD'): 'C',

    ('CC', 'CD', 'CC'): 'C',
    ('CC', 'CD', 'CD'): 'C',
    ('CC', 'CD', 'DC'): 'C',
    ('CC', 'CD', 'DD'): 'C',

    ('CC', 'DC', 'CC'): 'C',
    ('CC', 'DC', 'CD'): 'C',
    ('CC', 'DC', 'DC'): 'C',
    ('CC', 'DC', 'DD'): 'C',

    ('CC', 'DD', 'CC'): 'C',
    ('CC', 'DD', 'CD'): 'C',
    ('CC', 'DD', 'DC'): 'C',
    ('CC', 'DD', 'DD'): 'C',

    ('CD', 'CC', 'CC'): 'C',
    ('CD', 'CC', 'CD'): 'C',
    ('CD', 'CC', 'DC'): 'C',
    ('CD', 'CC', 'DD'): 'C',

    ('CD', 'CD', 'CC'): 'C',
    ('CD', 'CD', 'CD'): 'C',
    ('CD', 'CD', 'DC'): 'C',
    ('CD', 'CD', 'DD'): 'C',

    ('CD', 'DC', 'CC'): 'C',
    ('CD', 'DC', 'CD'): 'C',
    ('CD', 'DC', 'DC'): 'C',
    ('CD', 'DC', 'DD'): 'C',

    ('CD', 'DD', 'CC'): 'C',
    ('CD', 'DD', 'CD'): 'C',
    ('CD', 'DD', 'DC'): 'C',
    ('CD', 'DD', 'DD'): 'C',

    ('DC', 'CC', 'CC'): 'C',
    ('DC', 'CC', 'CD'): 'C',
    ('DC', 'CC', 'DC'): 'C',
    ('DC', 'CC', 'DD'): 'C',

    ('DC', 'CD', 'CC'): 'C',
    ('DC', 'CD', 'CD'): 'C',
    ('DC', 'CD', 'DC'): 'C',
    ('DC', 'CD', 'DD'): 'C',

    ('DC', 'DC', 'CC'): 'C',
    ('DC', 'DC', 'CD'): 'C',
    ('DC', 'DC', 'DC'): 'C',
    ('DC', 'DC', 'DD'): 'C',

    ('DC', 'DD', 'CC'): 'C',
    ('DC', 'DD', 'CD'): 'C',
    ('DC', 'DD', 'DC'): 'C',
    ('DC', 'DD', 'DD'): 'C',

    ('DD', 'CC', 'CC'): 'C',
    ('DD', 'CC', 'CD'): 'C',
    ('DD', 'CC', 'DC'): 'C',
    ('DD', 'CC', 'DD'): 'C',

    ('DD', 'CD', 'CC'): 'C',
    ('DD', 'CD', 'CD'): 'C',
    ('DD', 'CD', 'DC'): 'C',
    ('DD', 'CD', 'DD'): 'C',

    ('DD', 'DC', 'CC'): 'C',
    ('DD', 'DC', 'CD'): 'C',
    ('DD', 'DC', 'DC'): 'C',
    ('DD', 'DC', 'DD'): 'C',

    ('DD', 'DD', 'CC'): 'C',
    ('DD', 'DD', 'CD'): 'C',
    ('DD', 'DD', 'DC'): 'C',
    ('DD', 'DD', 'DD'): 'C',

}


def score_single(me, other, iterations=200):
    """
    Return the average score per turn for a player ina  single match against
    an opponent.
    """

    g = axelrod.Game()
    for _ in range(iterations):
        me.play(other)
    return sum([
        g.score(pair)[0]
        for pair in zip(me.history, other.history)
    ]) / iterations


def score_for(my_strategy_factory, iterations=200):
    """
    Given a function that will return a strategy, 
    calculate the average score per turn
    against all ordinary strategies. If the 
    opponent is classified as stochastic, then 
    run 100 repetitions and take the average to get 
    a good estimate. 
    """
    scores_for_all_opponents = []
    for opponent in axelrod.ordinary_strategies:
        print(opponent.name)
        # decide whether we need to sample or not
        if opponent.classifier['stochastic']:
            repetitions = 100
        else:
            repetitions = 1
        scores_for_this_opponent = []

        # calculate an average for this opponent
        for _ in range(repetitions):
            me = my_strategy_factory()
            other = opponent()
            # make sure that both players know what length the match will be
            # me.set_tournament_attributes(length=iterations)
            me.set_match_attributes(length=iterations)
            # other.set_tournament_attributes(length=iterations)
            other.set_match_attributes(length=iterations)

            scores_for_this_opponent.append(score_single(me, other, iterations))

        mean_vs_opponent = sum(scores_for_this_opponent) / len(scores_for_this_opponent)
        scores_for_all_opponents.append(mean_vs_opponent)

    # calculate the average for all opponents
    overall_average_score = sum(scores_for_all_opponents) / len(scores_for_all_opponents)
    return overall_average_score


# score = score_for(lambda: LookerUp(cooperator_table))

print(score_for(lambda: axelrod.LookerUp(cooperator_table)))
print(score_for(lambda: axelrod.Cooperator()))
