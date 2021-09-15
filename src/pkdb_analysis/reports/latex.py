import shutil
import subprocess
from pathlib import Path
from typing import List

import pandas as pd

from pkdb_analysis.core import Sid


def create_latex_report(
    output_dir: Path,
    substance_sids: List[str],
    substance_shorts: List[str],
    replacement_order: List[int] = None,
    citet: bool = False,
    number_header: bool = False,
):
    """Create latex table report.

    Latex files are created in the output_dir with the main latex file being
    'main.tex'. Conversion into pdf can be done for instance with pdflatex
        pdflatex main.tex

    """
    latex_tables = LatexTables(
        output_dir=output_dir,
        substance_sids=substance_sids,
        substance_shorts=substance_shorts,
        replacement_order=replacement_order,
    )
    latex_tables.create_pdf()
    latex_tables.create_latex(citet=citet, number_header=number_header)


class LatexTables:
    def __init__(
        self,
        output_dir: Path,
        substance_sids: List[str],
        substance_shorts: List[str],
        replacement_order: List[int] = None,
    ):
        """Reads TSV tables from output_path and creates corresponding latex tables."""
        # handle default arguments
        if replacement_order is None:
            replacement_order = range(len(substance_sids))

        self.output_dir = output_dir
        self.substance_sids = substance_sids
        self.substance_shorts = substance_shorts
        self.replacement_order = replacement_order

        # validation
        if len(substance_sids) != len(substance_shorts):
            raise ValueError(
                f"length of 'substance_sids' ({substance_sids}) must match length of short "
                f"names 'shorts' ({substance_shorts}), but '{len(substance_sids)} != {len(substance_shorts)}'."
            )
        if len(substance_sids) != len(replacement_order):
            raise ValueError(
                f"length of 'substance_sids' ({substance_sids}) must match length of "
                f"'replacement_order' ({replacement_order}), but '{len(substance_sids)} != {len(replacement_order)}'."
            )

    def create_pdf(self):
        """Create pdf using pdflatex.

        Requires working installation on system path.
        """
        self.create_latex()
        subprocess.run(["pdflatex", "main.tex"], cwd=self.output_dir)

    def create_latex(self, citet: bool = False, number_header: bool = False):
        """Creates all latex files."""
        self._create_latex_main()

        for table_key in ["studies", "timecourses", "pharmacokinetics"]:
            dfs = self._prepare_table(table_key=table_key)
            self._create_latex_tables(
                table_key=table_key, dfs=dfs, citet=citet, number_header=number_header
            )

    def _create_latex_main(self):
        """Create main latex files."""
        template_dir = Path(__file__).parent / "latex"
        for filename in ["main.tex", "tables.tex"]:
            shutil.copy(
                src=str(template_dir / filename),
                dst=str(self.output_dir / filename),
            )

        # update table captions
        with open(self.output_dir / "tables.tex", "r") as f:
            latex = f.read()
            latex = latex.replace(
                "SUBSTANCES",
                ", ".join(
                    [
                        f"{sid} ({short})"
                        for (sid, short) in zip(
                            self.substance_sids, self.substance_shorts
                        )
                    ]
                ),
            )

        with open(self.output_dir / "tables.tex", "w") as f:
            f.write(latex)

    def _prepare_table(self, table_key) -> List[pd.DataFrame]:
        """Prepares the tables"""
        all_measurements = ["individual", "group", "error", "plasma", "urine"]

        # read the table
        table_path = self.output_dir / f"{table_key}.tsv"
        if not table_path.exists():
            raise IOError(
                f"TSV file of table does not exist '{table_path}', create tables first."
            )

        df = pd.read_csv(table_path, sep="\t")  # , keep_default_na=False)
        # manual processing of table headers
        # delete columns
        del_keys = ["pubmed"]
        if table_key == "studies":
            delete_keys = del_keys + ["oral contraceptives"]
            rename_dict = {
                "body mass index": "bmi",
                "dosing amount": "dose",
                "dosing route": "route",
                "dosing form": "form",
                "quantification method": "method",
                "overnight fast": "fast",
                "abstinence alcohol": "alcohol",
            }

        elif table_key == "timecourses":
            delete_keys = del_keys
            for sid in self.substance_sids:
                del_keys = del_keys + [f"{sid}_plasma", f"{sid}_urine", f"{sid}_saliva"]

            rename_dict = {}
            for column in df.columns:
                key_original = column
                for k in self.replacement_order:
                    column = column.replace(
                        self.substance_sids[k], self.substance_shorts[k]
                    )

                rename_dict[key_original] = column

        elif table_key == "pharmacokinetics":
            delete_keys = del_keys
            for key in self.substance_sids:
                del_keys = del_keys + [f"{key}_plasma", f"{key}_urine", f"{key}_saliva"]

            rename_dict = {}
            for column in df.columns:
                key_original = column
                for k in self.replacement_order:
                    column = column.replace(
                        self.substance_sids[k], self.substance_shorts[k]
                    )
                rename_dict[key_original] = column

        # delete columns
        for del_key in delete_keys:
            del df[del_key]

        # rename columns
        df.rename(columns=rename_dict, inplace=True)

        # drop rows without entries
        df.dropna(thresh=3, inplace=True)  # only keep rows with at least 3 entries

        # replace NA
        df.fillna("", inplace=True)

        if table_key == "studies":
            dfs = [df]

        elif table_key == "timecourses":
            df_new = df[["PKDB", "name"]]
            for short in self.substance_shorts:
                for measurement in all_measurements:
                    df_new.loc[:, f"{short}_{measurement}"] = df.loc[
                        :, f"{short}_{measurement}"
                    ]

            # add empty columns for proper spacing
            for k in range(len(self.substance_shorts) - 1):
                offset = len(all_measurements) + 2
                value = len(all_measurements) + 1
                df_new.insert(
                    loc=offset + (k * value), column=f"empty{k}", value=[""] * len(df)
                )

            dfs = [df_new]

        elif table_key == "pharmacokinetics":
            df.replace(" ", "\hphantom{✓}", inplace=True)
            df_new = df.loc[:, ["PKDB", "name"]]
            for i, pkid in enumerate(
                ["auc", "clearance", "cmax", "kel", "thalf", "tmax", "vd"]
            ):
                for short in self.substance_shorts:
                    df_new.loc[:, f"{short}_{pkid}"] = (
                        df.loc[:, f"{short}_{pkid}_individual"]
                        + df.loc[:, f"{short}_{pkid}_group"]
                        + df.loc[:, f"{short}_{pkid}_error"]
                    )

                df_new.loc[:, f"empty{i}"] = [""] * len(df)

            # split into 2 tables (too big)
            split = 2 + (len(self.substance_sids) + 1) * 4 - 1
            end = 2 + (len(self.substance_sids) + 1) * 7 - 1
            df1 = df_new.iloc[:, 0:split]
            df2 = df_new.iloc[:, [0, 1] + list(range(split + 1, end))]
            dfs = [df1, df2]
        return dfs

    @staticmethod
    def latex_href(x):
        return "\href{https://alpha.pk-db.com/data/" + str(x) + "}{" + str(x) + "}"

    @staticmethod
    def count_true(series: pd.Series) -> int:
        return series.value_counts().get("✓", 0)

    def _create_latex_tables(
        self,
        table_key: str,
        dfs: List[pd.DataFrame],
        citet: bool = False,
        number_header: bool = False,
    ):
        """Convert dataframe to latex tables."""
        for k, df in enumerate(dfs):
            # create pandas latex content
            latex_path = self.output_dir / f"{table_key}.tex"

            if table_key == "pharmacokinetics":
                latex_path = self.output_dir / f"{table_key}_{k}.tex"
            if citet:
                df["name"] = df["name"].apply(lambda x: "\citet{" + str(x) + "}")
                df["PKDB"] = df["PKDB"].astype(str).apply(self.latex_href)
            pos = df.columns.get_loc("name")
            df.iloc[::2, pos] = df.iloc[::2, pos].apply(
                lambda x: r"\rowcolor{Lightgrey} " + str(x)
            )

            if number_header:
                header_row = {}
                for name in df.columns:
                    if name in {"PKDB"}:
                        header_row[name] = df[name].count()
                    elif name in {"name"}:
                        header_row[name] = "\#"
                    elif name in {"subjects", "groups"}:
                        header_row[name] = df[name].sum()
                    else:
                        header_row[name] = self.count_true(df[name])

                df = pd.concat(
                    [pd.DataFrame([header_row], columns=df.columns), df],
                    ignore_index=True,
                )

            if table_key == "studies":
                # rotate headers
                replacements = {
                    col: "\rotatebox{90}{" + col + "}"
                    for col in df.columns
                    if col not in ["PKDB", "name"]
                }
                df.rename(columns=replacements, inplace=True)

            with pd.option_context("max_colwidth", 1000):
                df.to_latex(
                    latex_path,
                    longtable=True,
                    index=False,
                    header=True,
                    caption=f"Overview of curated {table_key}. For each study the table shows which information was reported."
                    " Either, information was reported ($\checkmark$), partially reported ($\oslash$) or not "
                    "reported at all (whitespace).",
                    label=table_key,
                )

            # post processing
            with open(latex_path, "r") as f:
                latex = f.read()

            latex = latex.replace(r"textbackslash ", "")
            latex = latex.replace("\{", "{")
            latex = latex.replace("\}", "}")
            latex = latex.replace("⅟", "$⅟$")

            n_sids = len(self.substance_sids)

            if table_key == "timecourses":
                for k in self.replacement_order:
                    # remove prefixes
                    latex = latex.replace(f"{self.substance_shorts[k]}\_", "")

                # create a top header for each substance

                n_cols = 5
                latex = latex.replace(
                    "toprule",
                    "toprule\n\\rowcolor{white}\n "
                    + " & & "
                    + " & & ".join(
                        [
                            "\multicolumn{"
                            + str(n_cols)
                            + "}{c}{"
                            + sid
                            + " ("
                            + short
                            + ")}"
                            for sid, short in zip(
                                self.substance_sids, self.substance_shorts
                            )
                        ]
                    )
                    + "\\\\\n"
                    + " ".join(
                        [
                            "\cmidrule{"
                            + str(3 + k * (n_cols + 1))
                            + "-"
                            + str(3 + k * (n_cols + 1) + (n_cols - 1))
                            + "}"
                            for k in range(n_sids)
                        ]
                    )
                    + "\n\\rowcolor{white}",
                )

                # rotate headers
                for measurement in [
                    "individual",
                    "group",
                    "error",
                    "plasma",
                    "urine",
                    "saliva",
                ]:
                    latex = latex.replace(
                        measurement, r"\rotatebox{90}{" + measurement + "}"
                    )

                # remove headers of spacing columns
                for k in range(len(self.substance_shorts) - 1):
                    latex = latex.replace(f"empty{k}", "")

            if table_key == "pharmacokinetics":
                for pkid in ["auc", "clearance", "cmax", "kel", "thalf", "tmax", "vd"]:
                    latex = latex.replace(f"\_{pkid}", "")

                # create top headers for each pk parameter

                if k == 0:
                    pk_keys = ["auc", "clearance", "cmax", "kel"]
                else:
                    pk_keys = ["thalf", "tmax", "vd"]

                latex = latex.replace(
                    "toprule",
                    "toprule\n\\rowcolor{white}\n"
                    + "& &"
                    + "& &".join(
                        [
                            "\multicolumn{" + str(n_sids) + "}{c}{" + pk + "}"
                            for pk in pk_keys
                        ]
                    )
                    + "\\\\\n"
                    + " ".join(
                        [
                            "\cmidrule{"
                            + str(3 + k * (n_sids + 1))
                            + "-"
                            + str(3 + k * (n_sids + 1) + (n_sids - 1))
                            + "}"
                            for k in range(len(pk_keys))
                        ]
                    )
                    + "\n\\rowcolor{white}",
                )

            # remove the empty columns
            for k in range(10):
                latex = latex.replace(f"empty{k}", "")

            with open(latex_path, "w") as f:
                f.write(latex)

        def _post_processing2():
            """Long tables and pubmed ids."""
