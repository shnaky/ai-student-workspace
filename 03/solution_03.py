import numpy as np


def mc_random_Q(simulator):
    """
    Please modify the body of this function according to the description in exercise 3.1
    """
    K = simulator.getNumActions()
    Q_values = np.zeros(K, dtype=float)
    actions = [-1, 1]
    n_a = np.zeros(K, dtype=int)

    for n in range(K):
        y = simulator.reset()
        # print(simulator.state)
        a = actions[n]
        # print("a: {}".format(a))
        r, y, done = simulator.step(a)

        while True:
            # print("actions.index: {}".format(actions.index(a)))
            n_a[n] += 1
            Q_values[n] += r
            # print(n_a[actions.index(a)])

            if done:
                break

            a = np.random.choice(actions)
            r, y, done = simulator.step(a)
            # print("r, y, done: {} {} {}".format(r, y, done))

        # print(n_a)
        # print(Q_values)
    Q_values /= n_a
    # print(n_a)
    # print("Q_values: {}".format(Q_values))
    return Q_values


def mc_uct_Q(simulator):
    """
    Please modify the body of this function according to the description in exercise 3.2
    """
    raise NotImplementedError
