import numpy as np


class KptsController:
    def __init__(self, kpts, scheme='uniform', step=1):
        self.value = kpts
        self.scheme = scheme
        self.step = step
        self.type = 'KPOINTS'

    def update(self):
        if self.scheme == 'uniform':
            for i in range(self.step):
                self.value = np.add(self.value, [1, 1, 1])

        return self.value
