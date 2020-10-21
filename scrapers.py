#!/bin/bash
import logging

from requests_html import HTMLSession

DRUGBANK_URL = "http://go.drugbank.com/drugs/"
# Find a good way here to handle "Unknown" action badge once more data is required
ACTIONS_XPATH = "//div[@class='badge badge-pill badge-action']"
GENE_NAME_XPATH = "//dt[@id='gene-name']/following-sibling::dd"
SMILES_XPATH = "/html/body/main/div/div[1]/div[2]/div[2]/dl[6]/dd[6]"
SYNONYMS_XPATH = "/html/body/main/div/div[1]/div[2]/div[2]/dl[1]/dt[7]/following-sibling::dd/ul/*"
TARGETS_XPATH = "/html/body/main/div/div[1]/div[2]/div[2]/div[1]/div/*"


class DrugBankCommon(object):
    def identifiers(self, response):
        try:
            identifiers = []
            for identifier in response.html.xpath(SYNONYMS_XPATH):
                identifiers.append(identifier.text)
            return identifiers
        # Should add more specific error handling here
        except Exception:
            logging.fatal("Error parsing alternate identifiers.")


    def SMILES(self, response):
        # We have to render javascript here to avoid (presumably) CloudFlare email obfuscation.
        # SMILES strings preceding @ characters are probably incorrectly classified as emails by CloudFlare.
        #
        # Details: https://support.cloudflare.com/hc/en-us/articles/200170016-What-is-Email-Address-Obfuscation-
        response.html.render()
        try:
            return response.html.xpath(SMILES_XPATH)[0].text
        # Should add more specific error handling here
        except Exception:
            logging.fatal("Error parsing SMILES string.")

    def targets(self, response):
        try:
            targets = []
            for target in response.html.xpath(TARGETS_XPATH):
                action = target.xpath(ACTIONS_XPATH)
                gene_name = target.xpath(GENE_NAME_XPATH)
                if action == [] and gene_name == []:
                    continue
                targets.append(
                    {
                        "action": action[0].text if not action == [] else "Unknown",
                        "gene_name": gene_name[0].text if not gene_name == [] else "Unknown"
                    }
                )
            return targets
        # Should add more specific error handling here
        except Exception:
            logging.fatal("Error parsing targets.")


class DrugBankScraper(DrugBankCommon):
    def __init__(self):
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = HTMLSession()
        return self._session

    def get_by_dbid(self, dbid):
        return self.session.get(f"{DRUGBANK_URL}{dbid}")

    def get_metadata_by_dbid(self, dbid):
        response = self.get_by_dbid(dbid)
        return {
            "identifiers": self.identifiers(response),
            "SMILES": self.SMILES(response),
            "targets": self.targets(response)
        }

"""
class AsyncDrugBankScraper(DrugBankCommon):
    # TODO: Implement this class when/if you want to scrape more data more quickly
    #       using async scraping.

    def __init__(self):
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = AsyncHTMLSession()
        return self._session

    async def get_by_dbid(self, dbid):
        return self.session.get(f"{DRUGBANK_URL}{dbid}")

    async def wait_for_responses(self):
        ...

"""
