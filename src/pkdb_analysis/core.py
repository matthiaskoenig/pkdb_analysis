"""
Definition of core objects.
"""
from dataclasses import dataclass
from pathlib import Path
import pandas as pd


class Core:
    def __init__(self, source: Path):
        self.source = source
        self.sids = list(pd.read_csv(source).sid)


@dataclass(frozen=True)
class Sid:
    """PK-DB sid.
    Mainly used for type checking, later on for validation.
    """
    sid: str
    core: Core


    def __post_init__(self):
        if  self.sid not in self.core.sids:
            raise ValueError(f"{self.sid} is not in info_nodes [{self.core.source}]")



