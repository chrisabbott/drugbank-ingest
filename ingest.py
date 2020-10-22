import click
import logging
import psycopg2
import pprint
import yaml

from db import DrugBankDB
from scrapers import DrugBankScraper

logging_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

TABLES = (
    """
    CREATE TABLE drugs (
        dbid INTEGER PRIMARY KEY NOT NULL,
        SMILES VARCHAR(1000)
    )
    """,
    """
    CREATE TABLE identifiers (
        dbid INTEGER NOT NULL,
        identifier VARCHAR(1000),
        PRIMARY KEY(dbid, identifier)
    )
    """,
    """
    CREATE TABLE targets (
        dbid INTEGER NOT NULL,
        target_gene VARCHAR(1000) NOT NULL,
        target_action VARCHAR(1000),
        PRIMARY KEY(dbid, target_gene)
    )
    """
)


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

    # Get DB and attach to click context object
    ctx.obj['db'] = DrugBankDB()


@cli.command("create-tables", short_help="Create tables for Drugs, Identifiers, and Targets")
@click.pass_context
def create_tables(ctx):
    db = ctx.obj['db']
    logging.info(f"Creating tables ...")
    for new_table in TABLES:
        db.cursor.execute(new_table)
    db.cursor.close()
    db.conn.commit()
    logging.info(f"Done.")


@cli.command("scrape-single", short_help="Scrape an individual drug from DrugBank, used for testing")
@click.argument("dbid", type=str)
@click.pass_context
def scrape_single(ctx, dbid):
    scraper = ctx.obj['scraper']
    logging.info(f"Scraping {dbid} ...")
    logging.info(pprint.pformat(scraper.get_metadata_by_dbid(dbid)))
    logging.info(f"Done.")


@cli.command("scrape-all", short_help="Scrape all drugs in config from DrugBank, used for testing")
@click.pass_context
def scrape_all(ctx):
    scraper = ctx.obj['scraper']
    dbids = ctx.obj['dbids']
    for dbid in dbids:
        logging.info(f"Scraping {dbid} ...")
        dbid_metadata = scraper.get_metadata_by_dbid(dbid)
        logging.info(pprint.pformat(dbid_metadata))
    logging.info(f"Done.")


@cli.command("scrape-and-insert-all",
             short_help="Scrape all drugs in config from DrugBank and insert into respective tables")
@click.pass_context
def scrape_and_insert_all(ctx):
    scraper = ctx.obj['scraper']
    dbids = ctx.obj['dbids']
    db = ctx.obj['db']

    for dbid in dbids:
        logging.info(f"Scraping {dbid} ...")
        dbid_metadata = scraper.get_metadata_by_dbid(dbid)

        # These inserts should definitely happen in their own class and should
        # be much more abstracted away, but I'm going to keep this quick and simple
        db.cursor.execute("INSERT INTO drugs VALUES (%s, %s)", (dbid[-5:], dbid_metadata["SMILES"]))

        for target in dbid_metadata["targets"]:
            db.cursor.execute("INSERT INTO targets VALUES (%s, %s, %s)", (
                dbid[-5:], target["gene_name"], target["action"]))

        for identifier in dbid_metadata["identifiers"]:
            db.cursor.execute("INSERT INTO identifiers VALUES (%s, %s)", (dbid[-5:], identifier))

        logging.info(pprint.pformat(dbid_metadata))

    db.cursor.close()
    db.conn.commit()
    logging.info(f"Done.")


if __name__ == '__main__':
    cli()
