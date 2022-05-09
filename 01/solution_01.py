import numpy as np

def maximize_mean(mu_vector, sigma_vector):
    """
    Please modify the body of this function according to the description in exercise 1.1.1
    """
    return np.argmax(mu_vector)

def maximize_ucb(mu_vector, sigma_vector):
    """
    Please modify the body of this function according to the description in exercise 1.1.2
    """

    return np.argmax(mu_vector + 2 * sigma_vector)

def maximize_utility(mu_vector, sigma_vector, utility_function):
    """
    Please modify the body of this function according to the description in exercise 1.1.3
    """

    # sample size
    n = 1000
    # utility mean vector approximation
    approx_mean_vector = np.zeros(mu_vector.size)

    # Getting samples for every A
    for i in range(mu_vector.size):
        print('size of samples: {}'.format(int((n / mu_vector.size))))
        samples = np.random.normal(mu_vector[i], sigma_vector[i], int((n / mu_vector.size)))
        util_res = utility_function(samples)
        approx_mean_vector[i] = (1/n) * np.sum(util_res)
    
    return np.argmax(approx_mean_vector)

def maximize_mean_using_simulator(simulator, A, n):
    """
    Please modify the body of this function according to the description in exercise 1.2
    """

    # every probability outcome saved in array
    machine_outcomes = np.zeros((A, n))
    amounts_played = np.zeros(A, dtype=np.int64)
    mu_vector = np.zeros(A)
    #even though ucb is not needed it is still being calculated :)
    ucb_vector = np.zeros(A)
    

    # Init: play each machine once to get first porbability
    for a in range(A):
        machine_outcomes[a][0] = simulator(a)
        amounts_played[a] = amounts_played[a] + 1
        mu_vector[a] = mu_value_calc(1, machine_outcomes[a])
        ucb_vector = update_ucb(amounts_played, np.sum(amounts_played), mu_vector)


    # play the rest of queries allowed
    for a in range(n - A):
        # get machine with max ucb
        max_ucb_index = np.argmax(ucb_vector)  
        # play the machine
        machine_outcomes[max_ucb_index][amounts_played[max_ucb_index]] = simulator(max_ucb_index)
        amounts_played[max_ucb_index] = amounts_played[max_ucb_index] + 1
        mu_vector[max_ucb_index] = mu_value_calc(amounts_played[max_ucb_index], machine_outcomes[max_ucb_index])
        ucb_vector = update_ucb(amounts_played, np.sum(amounts_played), mu_vector)

    return  np.argmax(mu_vector) 


# Helper Functions for maximize_mean_using_simulator
def mu_value_calc(amounts_played, machine_outcomes):
    return (1/amounts_played) * np.sum(machine_outcomes)

def update_ucb(amounts_played, amounts_played_total, mu_vector):
    new_ucb = np.zeros(amounts_played.size)
    for n in range(amounts_played.size):
        if amounts_played[n] != 0:
            new_ucb[n] = mu_vector[n] + np.sqrt((2 * np.log(amounts_played_total))/amounts_played[n])

    return new_ucb