# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from .models import OvertimeRow

class OvertimeModelTests(TestCase):

    def test_last_paycycle_function_actually_works(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_date = OvertimeRow(date=time)
        self.assertIs(future_date.last_paycycle(), False)