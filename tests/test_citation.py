from pathlib import Path

import pkpdutils

CITATION = Path(__file__).parent.parent / "CITATION.cff"


def test_citation_version() -> None:
    # bump-my-version updates the `version` of the software; the `cff-version`
    # is the version of the citation file format and must stay a valid one
    lines = CITATION.read_text(encoding="utf-8").splitlines()
    assert f'version: "{pkpdutils.__version__}"' in lines
    assert "cff-version: 1.2.0" in lines
