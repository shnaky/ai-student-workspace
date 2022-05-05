"""
Test cases for you to check your solutions.
run by typing `pytest` in the task folder.
Do not change the content of this file!
"""
import numpy as np
import pytest

from solution_01 import maximize_mean, maximize_ucb, maximize_utility, maximize_mean_using_simulator

class UtilityFunctionClass():
    """
    Base class for utility functions used in these tests.
    This class simply provides a counter that ensures that
    the function is not called more often that n=1000 times.
    The function object that will be input to your solution
    algorithm is the method >>UtilityFunctionClass.call<<
    """
    def __init__(self):
        self.counter = 0

    def increment_counter(self, x):
        """
        Helper method
        """
        try:
            # for arrays, increment by number of elements
            self.counter += sum(x.shape)
        except AttributeError:
            # for floats, increment by 1
            self.counter += 1

        if self.counter > 1000:
            raise Exception("You exceeded the maximum allowed number of queries")

    def call(self, x):
        """
        Abstract implementation of function call at real value x
        Returns real value y, and increments counter.
        """
        raise NotImplementedError

class UtilityFunctionClass1(UtilityFunctionClass):
    """
    Utility functions: Test case 1
    """
    def call(self, x):
        """
        This function actually returns x itself.
        How do your results here compare to 1.1.1?
        Obviously, you could calculate the utility analytically in this case.
        But of course, your solver must work for any utility function, and can't
        rely on analytical solutions.
        """
        self.increment_counter(x)
        return x

class UtilityFunctionClass2(UtilityFunctionClass):
    """
    Utility functions: Test case 2
    """
    def call(self, x):
        """
        This function is a Gaussian.
        You could calculate the utility analytically in this case.
        But of course, your solver must work for any utility function, and can't
        rely on analytical solutions.
        """
        self.increment_counter(x)
        return 42.*np.exp(-x**2)

class UtilityFunctionClass3(UtilityFunctionClass):
    """
    Utility functions: Test case 3
    """
    def call(self, x):
        """
        A Polynomial
        """
        self.increment_counter(x)
        return 2.1*x**5 - 1.2*x**4 + 0.9*x**2 - 0.8*x + 1.1

class UtilityFunctionClass4(UtilityFunctionClass):
    """
    Utility functions: Test case 4
    """
    def call(self, x):
        """
        The logarithm of |x+1|
        """
        self.increment_counter(x)
        return np.log(np.abs(x+1))

class SimulatorBase():
    """
    Simulator: Base class
    """
    def __init__(self, n):
        self.counter = 0
        self.n = n
    
    def increment_counter(self):
        """
        Helper method
        """
        self.counter += 1

        if self.counter > self.n:
            raise Exception("You exceeded the maximum allowed number of queries")

    def simulate_outcome(self, a):
        """
        Simulate the outcome of action a
        """
        raise NotImplementedError

class DeterministicSimulator(SimulatorBase):
    """
    Deterministic return
    """
    def __init__(self, n):
        super().__init__(n)
        self.deterministic_returns = np.array([
            0.2, 0.4, 0.6, 0.1, 0.0, 0.3
        ])

    def simulate_outcome(self, a):
        if hasattr(a, "__len__"):
            raise Exception("Action a is non-scalar")
        self.increment_counter()
        return self.deterministic_returns[a]

class BinarySimulator(SimulatorBase):
    """
    Return 0 with probability p_a
    Return 1 with probability 1 - p_a
    p_a depends on action a
    """
    def __init__(self, n):
        super().__init__(n)
        self.A = 5

    def simulate_outcome(self, a):
        self.increment_counter()
        if a==0:
            return float(
                np.random.rand() > 0.7
            )
        elif a==1:
            return float(
                np.random.rand() > 0.1
            )
        elif a==2:
            return float(
                np.random.rand() > 0.5
            )
        elif a==3:
            return float(
                np.random.rand() > 0.9
            )
        elif a==4:
            return float(
                np.random.rand() > 0.3
            )
        else:
            raise Exception("Invalid action a")

class PiecewiseUniformSimulator(SimulatorBase):
    """
    Piecewise uniform distribution
    """
    def __init__(self, n):
        super().__init__(n)
        self.A = 5

    def simulate_outcome(self, a):
        self.increment_counter()
        if a==0:
            border = 0.9
            p_left = 0.5
        elif a==1:
            border = 0.1
            p_left = 0.5
        elif a==2:
            border = 0.9
            p_left = 0.05
        elif a==3:
            border = 0.5
            p_left = 0.05
        elif a==4:
            border = 0.96
            p_left = 0.99
        else:
            raise Exception("Invalid action a")

        if np.random.rand() < p_left:
            return border * np.random.rand()
        return border + (1-border) * np.random.rand()

@pytest.mark.parametrize(
    "mu_vector,sigma_vector,best_action",
    [
        (
            np.array([ 0.7 , -0.28, -0.52, -0.99, -0.96,  0.19,  0.46, -0.96,  0.91, -0.11]),
            np.array([0.77, 0.92, 0.65, 0.5 , 0.82, 0.63, 0.07, 0.96, 0.41, 0.9 ]),
            8
        ),
        (
            np.array([ 0.4 ,  0.1 , -0.38]),
            np.array([0.49, 0.33, 0.02]),
            0
        ),
        (
            np.array([-0.76, -0.15,  0.15,  0.32]),
            np.array([0.2, 0.13, 0.01, 0.23]),
            3
        ),
        (
            [-0.13, -0.02, -0.14,  0.12, -0.13,  0.16, -0.15, -0.01, -0.04],
            [1.07, 1.13, 0.69, 0.71, 1.09, 0.15, 0.99, 0.15, 0.7],
            5
        )
    ]
)
def test_maximize_mean(mu_vector, sigma_vector, best_action):
    """
    Test cases for exercise 1.1.1
    """
    assert best_action == maximize_mean(mu_vector, sigma_vector)

@pytest.mark.parametrize(
    "mu_vector,sigma_vector,best_action",
    [
        (
            np.array([-0.8, -0.01, -0.2, 0.94, -0.59, -0.79, -0.8, -0.52]),
            np.array([1.1, 0.69, 0.13, 0.77, 0.44, 0.6, 0.26, 0.48]),
            3
        ),
        (
            np.array([0.17, -0.19, -0.05, 0.23, -0.17, -0.04, -0.21, -0.08, 0.02]),
            np.array([0.04, 0.1, 0.08, 0.1, 0.04, 0., 0.06, 0., 0.09]),
            3
        ),
        (
            np.array([ 0., -0.14, -0.14]),
            np.array([0.4, 0.37, 0.1]),
            0
        ),
        (
            np.array([0.59, -0.4, 0.6]),
            np.array([1.37, 0.22, 1.47]),
            2
        )
    ]
)
def test_maximize_ucb(mu_vector, sigma_vector, best_action):
    """
    Test cases for exercise 1.1.2
    """
    assert best_action == maximize_ucb(mu_vector, sigma_vector)

@pytest.mark.parametrize(
    "mu_vector,sigma_vector,utility_function_class,best_action",
    [
        (
            np.array([-0.8, -0.01, -0.2, 0.94, -0.59, -0.79, -0.8, -0.52]),
            np.array([1.1, 0.69, 0.13, 0.77, 0.44, 0.6, 0.26, 0.48]),
            UtilityFunctionClass1,
            3
        ),
        (
            np.array([0.17, -0.19, -0.05, 0.23, -0.17, -0.04, -0.21, -0.08, 0.02]),
            np.array([0.04, 0.1, 0.08, 0.1, 0.04, 0., 0.06, 0., 0.09]),
            UtilityFunctionClass2,
            5
        ),
        (
            np.array([ 0., -0.14, -0.14]),
            np.array([0.4, 0.37, 0.1]),
            UtilityFunctionClass3,
            2
        ),
        (
            np.array([0.59, -0.4, 6.9]),
            np.array([1.37, 0.22, 1.47]),
            UtilityFunctionClass4,
            2
        )
    ]
)
def test_maximize_utility(mu_vector, sigma_vector, utility_function_class, best_action):
    """
    Test cases for exercise 1.1.3
    """
    # Instantiate function class (this sets counter to 0),
    # and then get function object.
    # Notice that the code here says ".call", not ".call()"
    # In other words, utility_function is a function object,
    # not the number that the function returns
    utility_function = utility_function_class().call

    assert best_action == maximize_utility(mu_vector, sigma_vector, utility_function)

test_cases = []

# 2 test cases for DeterministicSimulator
for n in [100, 10]:
    # instantiate simulator
    simulator_object = DeterministicSimulator(n)
    A = len(simulator_object.deterministic_returns)
    simulator = simulator_object.simulate_outcome

    # create input
    test_cases.append((
        simulator,
        A,
        n,
        2
    ))

# 2 test cases for BinarySimulator
for n in [1000, 200]:
    # instantiate simulator
    simulator_object = BinarySimulator(n)
    A = simulator_object.A
    simulator = simulator_object.simulate_outcome

    # create input
    test_cases.append((
        simulator,
        A,
        n,
        1
    ))

# 2 test cases for PiecewiseUniformSimulator
for n in [1000, 100]:
    # instantiate simulator
    simulator_object = PiecewiseUniformSimulator(n)
    A = simulator_object.A
    simulator = simulator_object.simulate_outcome

    # create input
    test_cases.append((
        simulator,
        A,
        n,
        2
    ))

@pytest.mark.parametrize(
    "simulator,A,n,best_action",
    test_cases
)
def test_maximize_mean_using_simulator(simulator, A, n, best_action):
    """
    Test cases for exercise 1.2
    """
    assert best_action == maximize_mean_using_simulator(simulator, A, n)
