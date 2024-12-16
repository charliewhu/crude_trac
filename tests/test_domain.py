import datetime as dt

import pytest
from src import domain


@pytest.fixture
def forcados():
    return domain.Grade("Forcados")


def test_get_present_value(forcados: domain.Grade):
    """
    Add a buy/sell Trade and calculate its present value based on
    market structure
    """

    bid = domain.Trade(
        grade=forcados,
        terms="FOB",
        location="Forcados Terminal",
        buy_sell_ind="bid",
        kb=950,
        formula="Dated",
        differential=-1.50,
        date=dt.datetime.now(),
        expiry=dt.datetime.now() + dt.timedelta(days=5),
        counterparty="A",
    )
    raise NotImplementedError
