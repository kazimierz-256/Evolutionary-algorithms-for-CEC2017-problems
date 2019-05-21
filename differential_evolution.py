import numpy as np

from util import get_new_point


class DifferentialEvolution:
    def __init__(self, dim, limit, mu, cec2017, fn_id):
        self.dim = dim
        self.limit = limit
        self.mu = mu
        self.cec2017 = cec2017
        self.fn_id = fn_id

    def optimize_min(self):
        points = [(np.random.multivariate_normal(np.zeros(self.dim), np.identity(self.dim) * 100), 0.0)] * self.mu
        history = list()

        for _ in range(self.limit):
            for i in range(self.mu):
                new_point = get_new_point(points, i, self.dim, do_crossover=True)
                evaluated = self.cec2017(self.fn_id, new_point.T)
                if evaluated is not None:
                    evaluated = evaluated[0]
                    history.append((new_point, evaluated))
                    _, fval_i = points[i]
                    if evaluated < fval_i:
                        points[i] = new_point, evaluated
