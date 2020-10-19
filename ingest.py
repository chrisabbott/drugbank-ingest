#!/bin/bash
import click
import logging
import psycopg2
import yaml

logging_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


@click.group()
@click.option("--verbosity", default="DEBUG", show_default=True)
@click.version_option()
@click.pass_context
def cli(ctx, verbosity):
    ctx.obj = {}
    logging.basicConfig(
        level=logging_levels[verbosity.upper()],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        ctx.obj.update(cfg)


@cli.command("scrape", short_help="Start scraping files from DrugBank")
@click.argument("subset", type=click.Choice(["default", "all"]))
@click.pass_context
def start(ctx, subset):
    logging.info(f"Scraping {subset} candidates ...")
    logging.info(f"Done.")


if __name__ == '__main__':
    cli()
