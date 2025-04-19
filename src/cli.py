import argparse
import datetime
import os
from utils import tree_schema

parser = argparse.ArgumentParser(description="OpenAI Operations")
subparsers = parser.add_subparsers(title="operations", dest="operation")

# Subparser for uploading a file
parser_search = subparsers.add_parser("search", help="Upload a file to OpenAI")
parser_search.add_argument("pattern", help="Glob pattern term")

parser_search.add_argument(
    "-n", "--num-results", type=int, default=10, help="Number of results to return"
)

# Subparser for fine-tuning a model
parser_insert = subparsers.add_parser("insert", help="Fine-tune a model with a file")
parser_insert.add_argument("pattern", help="Specify the filename for fine-tuning")

# Add flag to warn on change, default is False
parser_insert.add_argument(
    "--warn-on-change",
    "-w",
    action="store_true",
    help="Warn if the file has changed since it was last uploaded",
)


args = parser.parse_args()


vault_path = "~/Documents/obsidian-vaults/vaults/personalvault-1/"
if "~" in vault_path:
    vault_path = os.path.expanduser(vault_path)

if args.operation == "search":
    print(f"Search pattern: {args.pattern}")
    print("-" * 80)

    search_results = tree_schema(vault_path, args.pattern.replace("::", ":"))

    if "::" in args.pattern:
        with open(search_results[0]["file_path"], "r") as f:
            content = f.read()
        breakpoint()
    else:
        for row in search_results[: args.num_results]:
            print(row["title"])

    # breakpoint()
elif args.operation == "insert":
    print(f"insert")
