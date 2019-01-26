from flask import request, Response
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.doc.report.facility_report import FACILITY_REPORT_POST
from app.view.base_resource import ReportResource
from app.model import FacilityReportModel


class FacilityReportView(ReportResource):
    @swag_from(FACILITY_REPORT_POST)
    @jwt_required
    def post(self):
        student_id = get_jwt_identity()
        room = request.json['room']
        content = request.json['content']

        FacilityReportModel.post_facility_report(student_id, room, content)
        return Response('', 201)
