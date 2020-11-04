from abc import ABC, abstractmethod
from typing import List, Tuple

class AbstractAccumulatorManager(ABC):
    """
    An accumulator manager maintains the public state of the accumulator.
    Allows to add elements that should be in the domain of the hash function H, updating the state of the accumulator
    accordingly.
    Does not hold enough information to produce proofs; instead, whenever a new element is added, it should signal
    to listeners that an element was added, informing them of the new value of the counter, the value of the new
    element and the new root hash of the accumulator.
    """
    @abstractmethod
    def add(self, element: bytes):
        pass

class AbstractProver(ABC):
    @abstractmethod
    def element_added(self, k: int, x: bytes, r: bytes) -> None:
        """
        Listener for events from the accumulator manager.
        Records each added element x with index k, and the corresponding accumulator value r (corresponding to R_k).
        """
        pass

    @abstractmethod
    def prove(self, j: int) -> List[bytes]:
        """Produce a witness for the j-th element added to the accumulator."""
        pass

    @abstractmethod
    def prove_from(self, i: int, j: int) -> List[bytes]:
        """
        Produce a witness for the j-th element of the accumulator, starting from the root when the i-th element
        was added.
        """
        pass

class AbstractVerifier(ABC):
    @abstractmethod
    def verify(self, Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
        """
        Verify that `w` is a valid proof that the the `j`-th element added to the accumulator is `x`,
        given that the value of the accumulator after the `i`-th element was added is `Ri`.
        """
        pass


class AbstractAccumulatorFactory(ABC):
    @abstractmethod
    def create_accumulator(self, initial_elements: List[bytes] = []) -> Tuple[AbstractAccumulatorManager, AbstractProver, AbstractVerifier]:
        """Creates an accumulator manager, and the corresponding prover and verifier."""
        pass
