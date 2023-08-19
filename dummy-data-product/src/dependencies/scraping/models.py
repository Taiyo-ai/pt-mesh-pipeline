import datetime as dt
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RawTenders:
    tender_title: str
    tender_uri: str


@dataclass
class RawTender:
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
    payment_instruments: List[str]
    no_of_covers: int
    covers_information: List[str]
    tender_total_fee: int
    fee_payable_to: str
    fee_payable_at: str
    fee_exemption_allowed: bool
    emd_amount: int
    emd_fee_type: str
    emd_payable_to: str
    emd_exempt_allowed: bool
    emd_payable_at: str
    title: str
    description: str
    pre_qualification: str
    tender_value: int
    contract_type: str
    location: str
    should_allow_nda_tender: bool
    product_category: str
    bid_validity_in_days: int
    pincode: int
    allow_preferential_bidder: bool
    period_of_work_in_days: int
    bid_opening_place: str
    published_dt: dt.datetime
    sale_start_dt: dt.datetime
    sale_end_dt: dt.datetime
    bid_submission_start_dt: dt.datetime
    bid_submission_end_dt: dt.datetime
    # We cannot use this, because the download URIs are session based
    # and requires a captcha to actually download the files
    # which simple bots cannot do at the moment
    # tender_documents_url: str
    tender_invitation_authority_name: str
    tender_invitation_authority_address: str

    # Optional Defaults
    remarks: Optional[str] = None
    sub_category: Optional[str] = None
    clarification_start_dt: Optional[dt.datetime] = None
    clarification_end_dt: Optional[dt.datetime] = None
    emd_percentage: Optional[int] = None
    pre_bid_meeting_address: Optional[str] = None
    pre_bid_meeting_place: Optional[str] = None
    pre_bid_meeting_date: Optional[dt.datetime] = None
