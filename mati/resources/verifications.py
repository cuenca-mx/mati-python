from dataclasses import dataclass


@dataclass
class Verification:
    result: bool = None
    error: dict = None
