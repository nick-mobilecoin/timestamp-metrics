import argparse
import pandas as pd
import lmdb
from protos.blockchain import BlockSignatureData
from collections import defaultdict


def get_parser():
    parser = argparse.ArgumentParser(
        description="Get block times from a watcher database"
    )
    parser.add_argument("--db-path", help="Path to the watcher database", required=True)
    parser.add_argument(
        "--output-path",
        type=argparse.FileType("w"),
        help="Path to the output csv file",
        default="block_times.csv",
    )
    return parser


def open_database(db_path):
    env = lmdb.open(db_path, readonly=True, max_dbs=20)
    return env


# Not sure why, but I was getting stray capital letters in front of the urls at times.
# Also the urls have "\n<" in front of them.
def cleaned_url(url):
    position = url.find("https")
    return url[position:]


def get_block_times(env):
    signatures_db = env.open_db("watcher_db:block_signatures".encode())
    block_times = defaultdict(dict)
    with env.begin(db=signatures_db) as txn:
        cursor = txn.cursor()
        cursor.first()
        for key, value in cursor:
            index = int.from_bytes(key, "big")
            signature = BlockSignatureData().parse(value)
            url = cleaned_url(signature.src_url)
            assert index not in block_times[url]
            block_times[url][index] = signature.block_signature.signed_at
    return block_times


def format_block_times(block_times):
    max_block = max(len(v) for v in block_times.values())
    blocks = {}
    for url, values in block_times.items():
        times = []
        for i in range(1, max_block):
            times.append(values.get(i, None))
        blocks[url] = times

    return blocks


def write_csv(blocks, output_path):
    df = pd.DataFrame(blocks)
    df.to_csv(output_path)


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)
    env = open_database(args.db_path)
    block_times = get_block_times(env)
    blocks = format_block_times(block_times)
    write_csv(blocks, args.output_path)


if __name__ == "__main__":
    main()
