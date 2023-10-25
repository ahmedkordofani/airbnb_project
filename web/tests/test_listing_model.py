from seeds.seed_db import *


def test_search_by_date():
    seed_database()
    start_date = "2023-11-25"
    end_date = "2023-11-27"
    listings = Listing.get_by_date(start_date, end_date)
    assert len(listings) == 1


def test_search_all():
    seed_database()
    print(datetime.today)
    assert len(Listing.get_all()) == 2
