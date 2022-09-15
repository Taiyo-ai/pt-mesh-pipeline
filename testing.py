import unittest
from app import Scraper

class ActivityTests(unittest.TestCase):
  def test_scrape(self):
    scraper = Scraper('sample_body.html', 'test_events.csv')
    scraper.scrape()

    with open('sample_events.csv') as file:
      sample_csv = file.read()

    with open('test_events.csv') as file:
      test_csv = file.read()

    self.assertEqual(sample_csv, test_csv)

if __name__ == "__main__":
  unittest.main()