# %%
"""
Test cases for you to check your solutions.
run by typing `pytest` in the task folder.
Do not change the content of this file!
"""
import json
import gym
import numpy as np
import pytest

from solution_04 import q_learning

class FrozenLakeWrapper():
    """
    Thin wrapper around openAI gym API
    Works only for discrete state and action spaces
    """
    def __init__(self, gym_env):
        self.gym_env = gym_env
        self.num_steps = 0

    def getNumStates(self):
        """
        Return the number of states
        """
        return self.gym_env.observation_space.n

    def getNumActions(self):
        """
        Return the number of actions
        """
        return self.gym_env.action_space.n

    def reset(self):
        """
        Reset the environment and return observation
        """
        return self.gym_env.reset()

    def step(self, action):
        """
        Perform action and return reward, next_observation, done
        """
        if self.num_steps > 10_000:
            raise Exception("Maximum number of calls exceeded")

        self.num_steps += 1

        next_obs, reward, done, info = self.gym_env.step(action)
        return reward, next_obs, done

    def render(self):
        """
        Create render. Be careful not to call this in test_q_learning
        """
        self.gym_env.render()


with open("tests/data_public.json", 'r', encoding ='utf8') as data_file:
    test_params = json.load(data_file)
@pytest.mark.parametrize(
    "desc,Q_mean,Q_std",
    test_params
)
def test_q_learning(desc, Q_mean, Q_std):
    """
    For all actions in the start state, test that q_learning returns Q values that is
    less than 3 standard deviations from the true Q_mean.
    A correct implementation should return a Q value within these bounds in 99.7% of
    all cases, therefore the Q values for all 4 actions will be within these bounds at
    the same time in (99.7%)^4 = 98.8% of all cases.
    """
    Q_mean, Q_std = np.array(Q_mean), np.array(Q_std)

    env = FrozenLakeWrapper(
        gym.make(
            "FrozenLake-v1",
            desc=desc,
            is_slippery=True
        )
    )
    Q = q_learning(env)

    assert type(Q)==np.ndarray, "Object returned by q_learning is not a numpy array"
    assert Q.shape == (env.getNumStates(), env.getNumActions()), "Array returned has wrong shape (not SxA)"
    assert np.all(
        (
            np.abs(Q - Q_mean)/Q_std
        )[0, :] < 3
    )

# %%