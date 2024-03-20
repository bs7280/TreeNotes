import argparse
import datetime
import os
from utils import tree_schema

parser = argparse.ArgumentParser(description="OpenAI Operations")
subparsers = parser.add_subparsers(title="operations", dest="operation")

# Subparser for uploading a file
parser_upload = subparsers.add_parser("search", help="Upload a file to OpenAI")
parser_upload.add_argument("pattern", help="Glob pattern term")

# Subparser for fine-tuning a model
parser_fine_tune = subparsers.add_parser("insert", help="Fine-tune a model with a file")
parser_fine_tune.add_argument("pattern", help="Specify the filename for fine-tuning")

args = parser.parse_args()

vault_path = '~/Documents/personalvault-1/'
if '~' in vault_path:
    vault_path = os.path.expanduser(vault_path)

if args.operation == "search":
    print(f"Search pattern: {args.pattern}")
    print("-"*80)

    search_results = tree_schema(vault_path, args.pattern)

    for row in search_results[:15]:
        print(row['title'])

    #breakpoint()
elif args.operation == "insert":
    print(f"insert")