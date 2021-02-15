"""Definition of core objects."""
from dataclasses import dataclass
from pathlib import Path
from typing import Set

import pandas as pd


class Core:
    """This class mange the the source containing all info nodes.
    This source is used for validation."""

    def __init__(self, source: Path = None, sids: Set[str] = None):
        self.source = source
        if sids is None:
            self.sids = set(pd.read_csv(source).sid)
        else:
            self.sids = sids


@dataclass(frozen=True)
class Sid:
    """PK-DB sid.
    Mainly used for type checking, later on for validation.
    """

    sid: str
    core: Core

    def __str__(self):
        return self.sid

    def __post_init__(self):
        if self.sid not in self.core.sids:
            raise ValueError(f"{self.sid} is not in info_nodes [{self.core.source}]")
