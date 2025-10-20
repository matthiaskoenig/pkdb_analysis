# pkdb_analysis: PK-DB python interface
[![GitHub Actions CI/CD Status](https://github.com/matthiaskoenig/pkdb_analysis/workflows/CI-CD/badge.svg)](https://github.com/matthiaskoenig/pkdb_analysis/actions/workflows/main.yml)
[![Version](https://img.shields.io/pypi/v/pkdb_analysis.svg)](https://pypi.org/project/pkdb_analysis/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pkdb-analysis.svg)](https://pypi.org/project/pkdb-analysis/)
[![MIT License](https://img.shields.io/pypi/l/sbmlutils.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3997539.svg)](https://doi.org/10.5281/zenodo.3997539)

pkdb_analysis is a collection of python utilities to interact with
PK-DB https://pk-db.com via the available REST endpoints https://pk-db.com/api/v1/swagger/.

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3997539.svg)](https://doi.org/10.5281/zenodo.3997539)

## Installation

pkdb_analysis is available from [pypi](https://pypi.python.org/pypi/pkdb-analysis) and
can be installed via
```
pip install pkdb-analysis
```

## PK-DB endpoint

pkdb_analysis requires an existing PK-DB endpoint, which can be set by setting the
respective environment variables.

```bash
set -a && source .env.local
```

The public instances of PK-DB are available from
```bash
API_BASE=https://alpha.pk-db.com
API_BASE=https://pk-db.com
```

## License

- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)


## Funding

Matthias König is supported and by the German Research Foundation (DFG) within the Research Unit Programme FOR 5151
"`QuaLiPerF <https://qualiperf.de>`__ (Quantifying Liver Perfusion-Function Relationship in Complex Resection -
A Systems Medicine Approach)" by grant number 436883643 and by grant number
465194077 (Priority Programme SPP 2311, Subproject SimLivA).

Matthias König was supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054).

© 2018-2025 Jan Grzegorzewski & Matthias König.
