from service_api.manage import app
import json
import unittest


class AutoRestTests(unittest.TestCase):
    def test_get_metrics_smoke(self):
        request, response = app.test_client.get("/")
        self.assertEqual(response.status, 200)

        data = json.loads(response.text)
        self.assertEqual(data["message"], "Hello world!")

    def test_get_metrics_payments(self):
        request, response = app.test_client.get("/payments")
        self.assertEqual(response.status, 200)

    def test_get_metrics_filter(self):
        request, response = app.test_client.get("/payments/filter")
        self.assertEqual(response.status, 200)

    def test_get_metrics_payment_id(self):
        request, response = app.test_client.get(
            "/payment/0d571478-0953-4a20-a9f5-506974999228"
        )
        self.assertEqual(response.status, 200)

    def test_put_metrics_payment_id(self):
        request, response = app.test_client.put(
            "/payment/0d571478-0953-4a20-a9f5-506974999228"
        )
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
