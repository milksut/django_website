from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  # new
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  # new
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_template_content(self):  # new
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "<h1>Homepage</h1>")
