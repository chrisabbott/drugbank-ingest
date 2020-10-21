#!/bin/bash
import click
import logging
import psycopg2
import pprint
import yaml

from requests_html import HTMLSession
from scrapers import DrugBankScraper

logging_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


@click.group()
@click.option("--verbosity", default="INFO", show_default=True)
@click.version_option()
@click.pass_context
def cli(ctx, verbosity):
    ctx.obj = {}

    # Configure logging
    logging.basicConfig(
        level=logging_levels[verbosity.upper()],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Get config values and attach to click context object
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        ctx.obj.update(cfg)

    # Get scraper and attach to click context object
    ctx.obj['scraper'] = DrugBankScraper()


@cli.command("scrape-single", short_help="Scrape an individual drug from DrugBank")
@click.argument("dbid", type=str)
@click.pass_context
def scrape_single(ctx, dbid):
    scraper = ctx.obj['scraper']
    logging.info(f"Scraping {dbid} ...")
    logging.info(pprint.pformat(scraper.get_metadata_by_dbid(dbid)))
    logging.info(f"Done.")


@cli.command("scrape-all", short_help="Scrape all drugs in config from DrugBank")
@click.pass_context
def scrape_all(ctx):
    scraper = ctx.obj['scraper']
    dbids = ctx.obj['dbids']
    for dbid in dbids:
        logging.info(f"Scraping {dbid} ...")
        logging.info(pprint.pformat(scraper.get_metadata_by_dbid(dbid)))
    logging.info(f"Done.")


if __name__ == '__main__':
    cli()
