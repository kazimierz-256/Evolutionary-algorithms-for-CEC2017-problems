import numpy as np


class SingleEvaluation:
    def __init__(self, dim, limit, cec2017, fn_id):
        self.dim = dim
        self.limit = limit
        self.fn_id = fn_id
        self.cec2017 = cec2017

    def optimize_min(self):
        for _ in range(self.limit):
            x = np.random.rand(1, self.dim) * 200 - 100
            _ = self.cec2017(self.fn_id, x)[0]
