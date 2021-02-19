"""
dj-stripe TaxId Model Tests.
"""
from copy import deepcopy

from django.test import TestCase
from unittest.mock import patch

from djstripe.models import TaxId, Customer
from tests import (
    FAKE_TAX_ID,
    FAKE_CUSTOMER_WITH_TAX_ID,
    FAKE_CUSTOMER_WITHOUT_TAX_ID,
    AssertStripeFksMixin,
)

class TaxIdTest(AssertStripeFksMixin, TestCase):
    @patch("stripe.Customer.retrieve", return_value=deepcopy(FAKE_CUSTOMER_WITHOUT_TAX_ID))
    def test_sync_from_stripe_data(self, customer_mock):
        customer = Customer.sync_from_stripe_data(FAKE_CUSTOMER_WITHOUT_TAX_ID)
        self.assertEqual(customer.tax_ids.count(), 0)
        tax_id = TaxId.sync_from_stripe_data(deepcopy(FAKE_TAX_ID))
        self.assertEqual(tax_id.type, "eu_vat")
        self.assertEqual(tax_id.value, "DE123456789")
        self.assertEqual(customer.tax_ids.last(), tax_id)
