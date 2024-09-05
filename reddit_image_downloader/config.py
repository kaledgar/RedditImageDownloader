import argparse
from .constants import DEFAULT_USER_NAMES, DEFAULT_DOWNLOADS_PATH


def get_config_from_cli():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="""
        Give more output (corresponding to DEBUG logging level).
        """,
    )

    parser.add_argument(
        "-u",
        "--users",
        type=str,
        default=DEFAULT_USER_NAMES,
        nargs="+",
        help="""Give list of users""",
    )

    parser.add_argument(
        "-n",
        "--naming",
        type=str,
        choices=["created_utc", "id"],
        default="created_utc",
        help="""
        Pass naming convention of downloaded media files. You can choose: 
        id.format or created_utc.format (default)""",
    )

    parser.add_argument(
        "-rd",
        "--remove_duplicates",
        action="store_true",
        help="This flag removes the duplicates",
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=DEFAULT_DOWNLOADS_PATH,
        help="Directory where files will be downloaded",
    )

    cli_args = parser.parse_args()
    return cli_args
