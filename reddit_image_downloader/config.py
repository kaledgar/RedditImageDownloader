import argparse


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
    cli_args = parser.parse_args()
    return cli_args
