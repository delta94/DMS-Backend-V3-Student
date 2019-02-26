from datetime import date, timedelta

from flask import Response
from freezegun import freeze_time

from app.model.apply import ExtensionApplyModel
from test import TCBase, check_status_code
from test.request import ApplyRequest

tomorrow = str(date.today() + timedelta(1))


class TestDeleteExtension(TCBase, ApplyRequest):
    def setUp(self):
        super(TestDeleteExtension, self).setUp()

        self.extension_11_data = ExtensionApplyModel(
            student_id='test',
            time=11,
            class_=1,
            seat=16
        ).save()

        self.extension_12_data = ExtensionApplyModel(
            student_id='test',
            time=12,
            class_=1,
            seat=16
        ).save()

    @freeze_time(f"{tomorrow} 19:30:00")
    @check_status_code(200)
    def test_delete_extension_successful(self) -> Response:
        rv: Response = self.request_extension_delete(self.access_token, 11)

        self.assertIsNone(ExtensionApplyModel.get_extension_apply_status('test', 11))
        return rv

    @freeze_time(f"{tomorrow} 21:00")
    @check_status_code(409)
    def test_delete_11_extension_outside_time(self) -> Response:
        rv: Response = self.request_extension_delete(self.access_token, 11)

        return rv

    @freeze_time(f"{tomorrow} 22:30")
    @check_status_code(409)
    def test_delete_12_extension_outside_time(self) -> Response:
        rv: Response = self.request_extension_delete(self.access_token, 12)

        return rv
