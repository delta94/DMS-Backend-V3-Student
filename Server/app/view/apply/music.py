from flask import request, Response
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.doc.apply.music import MUSIC_GET, MUSIC_POST, MUSIC_DELETE
from app.view.base_resource import ApplyResource

from app.model import MusicApplyModel
from app.util.json_schema import json_type_validate, MUSIC_POST_JSON, MUSIC_DELETE_JSON


class MusicView(ApplyResource):
    @swag_from(MUSIC_GET)
    @jwt_required
    def get(self):
        return MusicApplyModel.get_music_apply_status()

    @json_type_validate(MUSIC_POST_JSON)
    @swag_from(MUSIC_POST)
    @jwt_required
    def post(self):
        student_id = get_jwt_identity()
        day = request.json['day']
        singer = request.json['singer']
        song_name = request.json['musicName']

        MusicApplyModel.post_music_apply(day, student_id, singer, song_name)
        return Response('', 201)

    @json_type_validate(MUSIC_DELETE_JSON)
    @swag_from(MUSIC_DELETE)
    @jwt_required
    def delete(self):
        student_id = get_jwt_identity()
        apply_id = request.json['applyId']

        MusicApplyModel.delete_music_apply(student_id, apply_id)
        return Response('', 200)
