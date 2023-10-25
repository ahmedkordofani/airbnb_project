from seeds.seed_db import *


def test_search_by_date():
    seed_database()
    start_date = datetime.strptime("16/11/2023", "%d/%m/%Y")
    end_date = datetime.strptime("18/11/2023", "%d/%m/%Y")
    listings = Listing.get_by_date(start_date, end_date)
    assert len(listings) == 1


def test_search_all():
    seed_database()
    assert len(Listing.get_all()) == 2
