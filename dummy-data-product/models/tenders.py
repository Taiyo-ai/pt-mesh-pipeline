import datetime as dt
from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple

PROJECT_OR_TENDER = Literal["P", "T"]


@dataclass
class Tender:
    published_date: dt.datetime
    opening_date: dt.datetime
    aug_id: str = ""
    original_id: str = ""
    project_or_tender: PROJECT_OR_TENDER = "P"
    name: str = ""
    description: str = ""
    source: str = ""
    status: str = ""  # Could it be an ENUM?
    budget: str = ""
    document_url: str = ""  # Link to the ZIP file containing all docs
    identified_sector: str = ""
    identified_subsector: str = ""
    country_name: str = ""
    country_code: str = ""
    region_name: str = ""
    region_code: str = ""
    state: str = ""

    # Optional Defaults
    location: Optional[str] = None
    county: Optional[str] = None
    locality: Optional[str] = None
    neighbourhood: Optional[str] = None

    # Defaults
    map_coordinates: Tuple[str, str] = field(default_factory=tuple)
    urls: List[str] = field(default_factory=list)
    sector: List[str] = field(default_factory=list)
    subsector: List[str] = field(default_factory=list)
