import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--fset",
    type=str,
    required=True,
    dest="fset",
    help="Absolute path to the set file of interest.",
)
parser.add_argument(
    "--fout",
    type=str,
    required=True,
    dest="fset",
    help="Absolute path to the output file.",
)
args = parser.parse_args()

df = pd.read_csv(args.fset)["Matrix"]
df.to_csv(args.fout, header=False, index=False)
