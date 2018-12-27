from app.doc.apply.stay import STAY_GET, STAY_POST
from app.view.base_resource import ApplyResource

from flasgger import swag_from


class StayView(ApplyResource):
    @swag_from(STAY_GET)
    def get(self):
        pass

    @swag_from(STAY_POST)
    def post(self):
        pass
