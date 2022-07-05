import numpy as np


def q_learning(env):
    """
    Please modify the body of this function according to the description in exercise 4.1
    """

    # Q-Table
    Q = np.zeros((env.getNumStates(), env.getNumActions()))
    alpha = 0.15  # Learning Rate
    gamma = 0.9  # Discount Factor
    epsilon = 0.15  # Epsilon-greedy (exploitation vs. exploration)
    episodes = 280  # Amount of episodes per game

    for ep in range(episodes):
        obs = env.reset()  # observation of agent
        done = False
        # By default, we consider our outcome to be a failure
        while not done:
            #  env.render()
            random = np.random.uniform(0, 1)
            # test we should exploit or explore
            if random < (1 - epsilon):
                if np.unique(Q[obs]).size == 1:
                    action = np.random.randint(0, env.getNumActions())
                else:
                    action = np.argmax(Q[obs])  # exploit
            else:
                action = np.random.randint(0, env.getNumActions())  # explore

            # take step with chosen action
            reward, next_obs, done = env.step(action)

            # calculate q-value
            Q[obs, action] = Q[obs, action] + alpha * (
                reward + gamma * np.amax(Q[next_obs]) - Q[obs, action]
            )
            # set next state
            obs = next_obs
    # np.set_printoptions(precision=5)
    # print(Q)
    return Q
