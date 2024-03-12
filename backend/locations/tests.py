from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from authx.models import CustomUser
from .models import Country, City, POI


class CountryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.country1 = Country.objects.create(
            name="Country 1",
            iso_code="C1",
            currency="Currency 1",
            primary_language="Language 1",
        )
        self.country2 = Country.objects.create(
            name="Country 2",
            iso_code="C2",
            currency="Currency 2",
            primary_language="Language 2",
        )

    def test_list_countries(self):
        self.client.force_login(self.user)
        response = self.client.get("/locations/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_country(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/locations/countries/{self.country1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Country 1")

    def test_create_country(self):
        self.client.force_login(self.user)
        data = {
            "name": "New Country",
            "iso_code": "NC",
            "currency": "New Currency",
            "primary_language": "New Language",
        }
        response = self.client.post("/locations/countries/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Country.objects.filter(name="New Country").exists())

    def test_update_country(self):
        self.client.force_login(self.user)
        data = {"name": "Updated Country"}
        response = self.client.put(
            f"/locations/countries/{self.country1.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.country1.refresh_from_db()
        self.assertEqual(self.country1.name, "Updated Country")

    def test_delete_country(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"/locations/countries/{self.country1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Country.objects.filter(id=self.country1.id).exists())


class CityViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.country = Country.objects.create(name="Country")
        self.city1 = City.objects.create(name="City 1", country=self.country)
        self.city2 = City.objects.create(name="City 2", country=self.country)

    def test_list_cities(self):
        self.client.force_login(self.user)
        response = self.client.get("/locations/cities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_city(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/locations/cities/{self.city1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "City 1")

    def test_create_city(self):
        self.client.force_login(self.user)
        data = {
            "name": "New City",
            "country": self.country.id,
            "population": 100000,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "region": "New Region",
        }
        response = self.client.post("/locations/cities/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(City.objects.filter(name="New City").exists())

    def test_update_city(self):
        self.client.force_login(self.user)
        data = {
            "name": "Updated City",
            "country": self.country.id,
        }
        response = self.client.put(
            f"/locations/cities/{self.city1.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.city1.refresh_from_db()
        self.assertEqual(self.city1.name, "Updated City")

    def test_delete_city(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"/locations/cities/{self.city1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(City.objects.filter(id=self.city1.id).exists())


class POIViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.country = Country.objects.create(name="Country")
        self.city = City.objects.create(name="City", country=self.country)
        self.poi1 = POI.objects.create(name="POI 1", city=self.city)
        self.poi2 = POI.objects.create(name="POI 2", city=self.city)

    def test_list_pois(self):
        self.client.force_login(self.user)
        response = self.client.get("/locations/pois/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_poi(self):
        self.client.force_login(self.user)
        response = self.client.get(f"/locations/pois/{self.poi1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "POI 1")

    def test_create_poi(self):
        self.client.force_login(self.user)
        data = {
            "name": "New POI",
            "description": "New POI Description",
            "city": self.city.id,
            "location_latitude": 40.7128,
            "location_longitude": -74.0060,
            "opening_hours": "New Opening Hours",
        }
        response = self.client.post("/locations/pois/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(POI.objects.filter(name="New POI").exists())

    def test_update_poi(self):
        self.client.force_login(self.user)
        data = {
            "name": "Updated POI",
            "city": self.city.id,
        }
        response = self.client.put(
            f"/locations/pois/{self.poi1.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.poi1.refresh_from_db()
        self.assertEqual(self.poi1.name, "Updated POI")

    def test_delete_poi(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"/locations/pois/{self.poi1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(POI.objects.filter(id=self.poi1.id).exists())
