from unittest import TestCase
from utils import scrapStudyAbroadApartments


class TestStudyAbroadApartmentsAccommodations(TestCase):
    def test_studyAbroadApartmentsAccommodations(self):
        filters = {'city': 'valencia'}
        data = scrapStudyAbroadApartments.studyAbroadApartmentsAccommodations(filters)
        self.assertEqual(data[0]['city'], 'madrid')
