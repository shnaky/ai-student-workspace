# %%
"""
Test cases for you to check your solutions.
run by typing `pytest` in the task folder.
Do not change the content of this file!
"""
import numpy as np
import pytest

from solution_03 import mc_random_Q, mc_uct_Q

class Simulator():
    """
    Abstract black-box simulator class
    """

    def reset(self):
        """
        Reset using initial state distribution
        """
        raise NotImplementedError

    def getNumActions(self):
        """
        Get number of possible discrete actions
        """
        raise NotImplementedError

    def step(self, a):
        """
        Perform step using action a
        """
        raise NotImplementedError

class IntegerDomainSimulator(Simulator):
    """
    Integer domain simulator
    """

    def __init__(
        self,
        winning_state,
        loosing_state,
        maximum_steps_per_episode=None
    ):
        self.counter = 0
        self.winning_state = winning_state
        self.loosing_state = loosing_state
        self.maximum_steps_per_episode=maximum_steps_per_episode

        self.reached_terminal = None
        self.reset()

    def getNumActions(self):
        return 2

    def reset(self):
        # unlock
        self.reached_terminal = False
        self.steps_current_episode = 0
        # initial state distribution
        self.state = np.random.randint(low=-3, high=4)

        # no observations
        y = 0

        return y

    def step(self, a):
        assert a in [-1, 1], "Action must be -1 or 1"

        if self.counter > 10_000:
            raise Exception("Maximum number of simulator steps exceeded")

        self.counter += 1
        self.steps_current_episode += 1
        assert not self.reached_terminal, "Terminal state reached"

        self.state += a

        # no observations
        y = 0

        # case 1: terminal state reached
        if (
            self.state == self.winning_state
        ) or (
            self.state == self.loosing_state
        ):
            self.reached_terminal = True
            done = True

            if self.state == self.winning_state:
                r = 1.0
            if self.state == self.loosing_state:
                r = -1.0

            return (r, y, done)

        # case 2: no terminal state, but maximum_steps_per_episode reached
        if self.maximum_steps_per_episode:
            if self.steps_current_episode >= self.maximum_steps_per_episode:
                done = True
                r = 0.0
                return (r, y, done)

        # case 3: neither terminal state nor maximum_steps_per_episode reached
        done = False
        r = 0.0
        return (r, y, done)

# %%
@pytest.mark.parametrize(
    "winning_state,loosing_state,Q_mean,Q_std",
    [
        ( -6 , 4 , np.array([-3.56296064e-04, -3.97406110e-01]) , np.array([0.06073885, 0.05870853]) ),
        ( 5 , -5 , np.array([-0.19641983,  0.19576237]) , np.array([0.0628305 , 0.05905241]) ),
        ( 7 , -8 , np.array([-0.07740874,  0.21129049]) , np.array([0.09782989, 0.09484061]) ),
        ( -8 , 6 , np.array([ 0.00429491, -0.28207604]) , np.array([0.09759289, 0.09458235]) ),
        ( 8 , -5 , np.array([-0.38403921, -0.08092717]) , np.array([0.06624262, 0.07687261]) ),
        ( -4 , 7 , np.array([0.44668177, 0.08733171]) , np.array([0.05446603, 0.07297614]) ),
        ( -6 , 7 , np.array([ 0.2355497 , -0.07717278]) , np.array([0.08515888, 0.08435123]) ),
        ( -7 , 7 , np.array([ 0.15776256, -0.13934671]) , np.array([0.09267629, 0.09690629]) ),
        ( -4 , 7 , np.array([0.45168461, 0.09855633]) , np.array([0.05362355, 0.06730769]) ),
        ( 8 , -8 , np.array([-0.12600653,  0.12765935]) , np.array([0.09972534, 0.11151803]) )
    ]
)
def test_mc_random_Q(winning_state, loosing_state, Q_mean, Q_std):
    """
    Test that mc_random_Q returns mean Q value that is less than 3 standard deviations
    from the true Q_mean.
    A correct implementation should return a Q value within these bounds in 99.7% of
    all cases, therefore the Q values for both actions will be within these bounds at
    the same time in (99.7%)^2 = 99.4% of all cases.
    """
    simulator = IntegerDomainSimulator(winning_state, loosing_state)
    assert np.all(np.abs(
        mc_random_Q(simulator) - Q_mean
    )/Q_std < 3)

# %%
@pytest.mark.parametrize(
    "winning_state,loosing_state,Q_mean,Q_std",
    [
        ( -6 , 8 , np.array([0.46379057, 0.17503184]) , np.array([0.06813978, 0.0818908 ]) ),
        ( -6 , 4 , np.array([0.43759629, 0.02758653]) , np.array([0.05648033, 0.08308253]) ),
        ( 4 , -4 , np.array([0.33930943, 0.716333  ]) , np.array([0.04264981, 0.02244342]) ),
        ( -4 , 6 , np.array([0.68856408, 0.42598926]) , np.array([0.02870114, 0.06163662]) ),
        ( 5 , -8 , np.array([0.25214662, 0.53983226]) , np.array([0.08643831, 0.05274133]) ),
        ( 7 , -7 , np.array([-0.006997  ,  0.28009587]) , np.array([0.09667225, 0.08122753]) ),
        ( -4 , 4 , np.array([0.71157609, 0.34776682]) , np.array([0.02386171, 0.03884361]) ),
        ( 4 , -7 , np.array([0.37525795, 0.66466592]) , np.array([0.0612568 , 0.02930077]) ),
        ( 5 , -5 , np.array([0.23566643, 0.53753233]) , np.array([0.07976742, 0.04464027]) ),
        ( 7 , -4 , np.array([-0.14012129,  0.22699837]) , np.array([0.08886999, 0.05878157]) )
    ]
)
def test_mc_uct_Q(winning_state, loosing_state, Q_mean, Q_std):
    """
    Test that mc_uct_Q returns mean Q value that is less than 3 standard deviations
    from the true Q_mean.
    A correct implementation should return a Q value within these bounds in 99.7% of
    all cases, therefore the Q values for both actions will be within these bounds at
    the same time in (99.7%)^2 = 99.4% of all cases.
    """
    simulator = IntegerDomainSimulator(winning_state, loosing_state)
    assert np.all(np.abs(
        mc_uct_Q(simulator) - Q_mean
    )/Q_std < 3)
