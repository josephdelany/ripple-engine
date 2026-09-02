"""countries.py -- the one country-code map (WS-R4): corpus `country.*` id <-> COW ccode/stateabb <-> ISO3.

Every loader maps through this table. A code the table does not know is reported by status.py under
`unmapped`, never silently dropped. The COW pairs are checked against the NMC file's own `stateabb`
column by tests/state/test_countries.py, so drift in this hand table is caught by the data.
"""
# corpus id : (COW ccode, COW stateabb, ISO3, name)
COUNTRIES = {
    "country.usa": (2, "USA", "USA", "United States"),
    "country.canada": (20, "CAN", "CAN", "Canada"),
    "country.panama": (95, "PAN", "PAN", "Panama"),
    "country.venezuela": (101, "VEN", "VEN", "Venezuela"),
    "country.ecuador": (130, "ECU", "ECU", "Ecuador"),
    "country.peru": (135, "PER", "PER", "Peru"),
    "country.chile": (155, "CHL", "CHL", "Chile"),
    "country.argentina": (160, "ARG", "ARG", "Argentina"),
    "country.hungary": (310, "HUN", "HUN", "Hungary"),
    "country.serbia": (345, "YUG", "SRB", "Serbia (COW 345 Yugoslavia/Serbia)"),
    "country.russia": (365, "RUS", "RUS", "Russia (COW 365 USSR/Russia)"),
    "country.ukraine": (369, "UKR", "UKR", "Ukraine"),
    "country.georgia": (372, "GRG", "GEO", "Georgia"),
    "country.azerbaijan": (373, "AZE", "AZE", "Azerbaijan"),
    "country.niger": (436, "NIR", "NER", "Niger"),
    "country.guinea": (438, "GUI", "GIN", "Guinea"),
    "country.nigeria": (475, "NIG", "NGA", "Nigeria"),
    "country.gabon": (481, "GAB", "GAB", "Gabon"),
    "country.congo_drc": (490, "DRC", "COD", "Congo, Dem. Rep."),
    "country.south_africa": (560, "SAF", "ZAF", "South Africa"),
    "country.libya": (620, "LIB", "LBY", "Libya"),
    "country.sudan": (625, "SUD", "SDN", "Sudan"),
    "country.iran": (630, "IRN", "IRN", "Iran"),
    "country.turkey": (640, "TUR", "TUR", "Turkey"),
    "country.iraq": (645, "IRQ", "IRQ", "Iraq"),
    "country.egypt": (651, "EGY", "EGY", "Egypt"),
    "country.lebanon": (660, "LEB", "LBN", "Lebanon"),
    "country.israel": (666, "ISR", "ISR", "Israel"),
    "country.saudi_arabia": (670, "SAU", "SAU", "Saudi Arabia"),
    "country.yemen": (679, "YEM", "YEM", "Yemen (COW 679 unified; 678 YAR before 1990)"),
    "country.kuwait": (690, "KUW", "KWT", "Kuwait"),
    "country.qatar": (694, "QAT", "QAT", "Qatar"),
    "country.uae": (696, "UAE", "ARE", "United Arab Emirates"),
    "country.kazakhstan": (705, "KZK", "KAZ", "Kazakhstan"),
    "country.china": (710, "CHN", "CHN", "China"),
    "country.taiwan": (713, "TAW", "TWN", "Taiwan"),
    "country.south_korea": (732, "ROK", "KOR", "South Korea"),
    "country.japan": (740, "JPN", "JPN", "Japan"),
    "country.india": (750, "IND", "IND", "India"),
    "country.myanmar": (775, "MYA", "MMR", "Myanmar"),
    "country.thailand": (800, "THI", "THA", "Thailand"),
    "country.vietnam": (816, "DRV", "VNM", "Vietnam (COW 816)"),
    "country.philippines": (840, "PHI", "PHL", "Philippines"),
    "country.indonesia": (850, "INS", "IDN", "Indonesia"),
}
# actors the state needs that the corpus does not (yet) name as country.* entities
EXTRA = {
    "country.gbr": (200, "UKG", "GBR", "United Kingdom"),
    "country.fra": (220, "FRN", "FRA", "France"),
    "country.deu": (255, "GMY", "DEU", "Germany"),
    "country.afg": (700, "AFG", "AFG", "Afghanistan"),
    "country.pak": (770, "PAK", "PAK", "Pakistan"),
    "country.syr": (652, "SYR", "SYR", "Syria"),
    "country.jor": (663, "JOR", "JOR", "Jordan"),
    "country.omn": (698, "OMA", "OMN", "Oman"),
    "country.bhr": (692, "BAH", "BHR", "Bahrain"),
    "country.dza": (615, "ALG", "DZA", "Algeria"),
    "country.ago": (540, "ANG", "AGO", "Angola"),
    "country.mex": (70, "MEX", "MEX", "Mexico"),
    "country.nor": (385, "NOR", "NOR", "Norway"),
    "country.bra": (140, "BRA", "BRA", "Brazil"),
    "country.col": (100, "COL", "COL", "Colombia"),
}
ALL = {**COUNTRIES, **EXTRA}
BY_CCODE = {v[0]: k for k, v in ALL.items()}
BY_ISO3 = {v[2]: k for k, v in ALL.items()}
BY_ABB = {v[1]: k for k, v in ALL.items()}
# COW codes that later became / were absorbed by a mapped state: map onto the successor id for the panel
ALIASES_CCODE = {678: "country.yemen"}


def from_ccode(c):
    try:
        c = int(c)
    except (TypeError, ValueError):
        return None
    return BY_CCODE.get(c) or ALIASES_CCODE.get(c)


def from_iso3(s):
    return BY_ISO3.get((s or "").upper())


def from_abb(s):
    return BY_ABB.get((s or "").upper())


def dyad_id(a, b):
    """dyad.<a>__<b> with the two corpus ids sorted (undirected)."""
    x, y = sorted([a, b])
    return f"dyad.{x.split('.', 1)[1]}__{y.split('.', 1)[1]}"
