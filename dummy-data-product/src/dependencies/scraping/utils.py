import json
from typing import Dict, Iterator

from bs4 import BeautifulSoup

from .models import RawTenders, RawTender
from .scraper import DataScraper


def list_raw_tenders(soup: BeautifulSoup) -> Iterator["RawTenders"]:
    """
    Yields tender lists from the given soup.

    Args:
        soup: The soup object parsed from the url
    """

    active_tenders = soup.find("table", attrs={"id": "activeTenders"})
    if active_tenders is None:
        raise RuntimeError("No tenders found in the soup")

    rows = active_tenders.find_all("tr")  # type: ignore  # bs4's typing hints are pretty bad
    if rows is None:
        raise RuntimeError("No tenders found in the soup")

    for tender in rows:
        tender_detail_page_element = tender.find("a", class_="link2")
        if tender_detail_page_element is None:
            raise RuntimeError(
                "Invalid data! Cannot find the detailed information on the tender"
            )

        tender_detail_page_url = tender_detail_page_element.attrs.get("href")
        if tender_detail_page_url is None:
            raise RuntimeError(
                "Invalid data! Cannot find the detailed information on the tender"
            )

        tender_title: str = tender_detail_page_element.text
        yield RawTenders(tender_title, tender_detail_page_url)

def fetch_tender(tender: RawTenders):
    """Fetches a single raw tender."""

    url = f"https://etenders.gov.in{tender.tender_uri}"
    scraper = DataScraper(url)
    soup = scraper.scrape()
    return RawTender.from_soup(soup)
