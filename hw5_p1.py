import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import scr.FigureSupport as Fig


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_reward(self):
        return self._gameRewards

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)


# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)

class OutType(Enum):
    """output types for plotted figures"""
    SHOW = 1    # show
    JPG = 2     # save the figure as a jpg file
    PDF = 3     # save the figure as a pdf file

def output_figure(plt, output_type, title):
    """
    :param plt: reference to the plot
    :param output_type: select from OutType.SHOW, OutType.PDF, or OutType.JPG
    :param title: figure title
    :return:
    """
    # output
    if output_type == OutType.SHOW:
        plt.show()
    elif output_type == OutType.JPG:
        plt.savefig(title+".png")
    elif output_type == OutType.PDF:
        plt.savefig(title+".pdf")


def graph_histogram(observations, title, x_label, y_label, output_type=OutType.SHOW, legend=None):
    """ graphs the histogram of observations
    :param observations: list of observations
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param output_type: select from OutType.SHOW, OutType.PDF, or OutType.JPG
    :param legend: string for the legend
    """

    fig = plt.figure(title)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.hist(observations,
             bins='auto',  #numpy.linspace(0, max(patient_survival_times), num_bins),
             edgecolor='black',
             linewidth=1)
    plt.xlim([min(observations), max(observations)])

    # add legend if provided
    if not (legend is None):
        plt.legend([legend])

    # output figure
    output_figure(plt, output_type, title)

graph_histogram(
    observations=games.get_reward(),
    title='Histogram of rewards for 1000 times',
    x_label='Rewards',
    y_label='Times',
    )

#The maximum reward should be 100*6-250 = 350, because we can get 6 "TTH" in 20 flips.
#The minimum reward should be 0*100 - 250 = -250
