import datetime as dt
from dataclasses import dataclass
from typing import Dict, List

from bs4 import BeautifulSoup, Comment


@dataclass
class TendersMetaData:
    tender_title: str
    tender_uri: str
    reference_no: str
    closing_dt: str
    bid_opening_dt: str


@dataclass
class BasicDetails:
    organisation_chain: str
    reference_number: str
    tender_id: str
    tender_type: str
    tender_category: str
    general_technical_evalauation_allowed: bool
    itemwise_technical_evalauation_allowed: bool
    payment_mode: str
    is_multi_currency_allowed_for_fee: bool
    is_multi_currency_allowed_for_boq: bool
    withdrawl_allowed: bool
    form_of_contract: str
    no_of_covers: int
    allow_two_stage_bidding: bool

    @staticmethod
    def from_soup(soup: BeautifulSoup):
        label_tds = soup.find_all("td", class_="textbold1")
        label_td = None
        for td in label_tds:
            if td.text.strip() == "Basic Details":
                label_td = td
                break

        if label_td is None:
            raise RuntimeError("Basic Details not found in the soup")


@dataclass
class PaymentInstructions:
    serial_number: int
    instrument_type: str


@dataclass
class CoversInformation:
    cover_no: int
    cover_type: str
    description: str
    document_type: str


@dataclass
class TenderFeeDetails:
    tender_fee: float
    fee_payable_to: str
    fee_payable_at: str
    fee_exemption_allowed: bool


@dataclass
class EMDFeeDetails:
    emd_amount: float
    emd_fee_type: str
    emd_payable_to: str
    emd_exempt_allowed: bool
    emd_payable_at: str


@dataclass
class WorkItemDetails:
    title: str
    description: str
    pre_qualification: str
    tender_value: str
    contract_type: str
    location: str
    should_allow_nda_tender: bool
    product_category: str
    bid_validity_in_days: int
    pincode: int
    allow_preferential_bidder: bool
    period_of_work_in_days: int
    bid_opening_place: str


@dataclass
class CriticalDetails:
    published_dt: dt.datetime
    sale_start_dt: dt.datetime
    sale_end_dt: dt.datetime
    bid_submission_start_dt: dt.datetime
    bid_submission_end_dt: dt.datetime


@dataclass
class TenderDocuments:
    document_type: str
    serial_no: int
    document_name: str
    description: str
    document_size: float  # in KB


@dataclass
class TenderInvitingAuthority:
    name: str
    address: str


@dataclass
class RawTender:
    basic_details: BasicDetails
    payment_instruments: List[PaymentInstructions]
    covers_information: List[CoversInformation]
    tender_fee_details: TenderFeeDetails
    emd_fee_details: EMDFeeDetails
    work_item_details: WorkItemDetails
    critical_details: CriticalDetails
    tender_documents: List[TenderDocuments]
    tender_inviting_authority: TenderInvitingAuthority

    @classmethod
    def from_soup(cls, soup: BeautifulSoup):
        """Create a raw tender object from the soup."""

        section_headers = soup.find_all("td", class_="textbold1")
        section_contents = soup.find_all("table", class_="tablebg")

        section_labels = [header.text.split(",")[0].strip().replace(" ", "_").lower() for header in section_headers]
        section_values = []
        for section in section_contents:
            caption_els = section.find_all("td", class_="td_caption")
            captions = [" ".join(caption.text.split()) for caption in caption_els]
            value_els = section.find_all("td", class_="td_field")
            values = [" ".join(value.text.split()) for value in value_els]
            section_values.append({caption: value for caption, value in zip(captions, values)})

        mapping: Dict[str, str] = {key: value for key, value in zip(section_labels, section_values)}
        """
        TODO: Load the mapping dict into `RawTender` dataclass to have pythonic representation of data
        i. Format the `mapping` data to match with the dataclasses defined structure
        ii. Format the _special_ data representation of nested lists for "Payment Instruments", "Covers Information"
        and "Tenders Documents" sections.
        """
        return mapping
