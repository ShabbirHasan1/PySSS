"""
    sss.py: An abstract class of secret sharing scheme objects
    Author: Jun Kurihara <kurihara at ieee.org>
"""

import secrets
import numpy as np
from typing import List
from abc import *


class SSS:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._secret = None
        self._shares = None
        self._share_index_list = None
        self._threshold = 0
        self._ramp = 0
        self._num = 0
        self.random = None

        self.orig_secret_size = 0

    # protected methods
    def _set_params(self, threshold: int, ramp: int, num: int) -> None:
        self._threshold = threshold
        self._ramp = ramp
        self._num = num

    def _generate_random(self, max_value, data_type) -> None:
        # Now random numbers are generated by os.urandom in secrets.SystemRandom
        # that is probably cryptographically secure.
        rng = secrets.SystemRandom()
        self.random = np.empty([self._threshold - self._ramp, int(self._secret.size / self._ramp)], data_type)
        self.random = np.vectorize(lambda a: rng.randint(0, max_value))(self.random).astype(data_type)

    # abstract methods
    @abstractmethod
    def initialize(self, threshold: int, ramp: int, num: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def generate_shares(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_secret(self, secret: np.ndarray) -> None:
        raise NotImplementedError()

    @abstractmethod
    def reconstruct_secret(self, orig_size: int) -> None:
        raise NotImplementedError()

    # public methods
    def set_external_shares(self, shares: List, index_list: List) -> None:
        assert len(shares) == len(index_list), "# of shares and # of indices are not same"

        self._shares = shares
        self._share_index_list = index_list[:self._threshold]

    def get_secret(self) -> np.ndarray:
        return self._secret

    def get_shares(self) -> np.ndarray:
        return self._shares
