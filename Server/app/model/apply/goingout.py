from datetime import datetime, timedelta
from typing import List

from app.exception import NoContentException, ApplyTimeException
from app.extension import db
from app.model.mixin import BaseMixin

going_out_status_message = [
    '외출 전',
    '외출 중',
    '복귀'
]


def str_to_datetime(string) -> dict:
    day = string[:6]
    now = datetime.now()
    year = str(now.year) + '-'

    go_out_date: datetime = datetime.strptime(year + day + string[6:11], '%Y-%m-%d %H:%M')
    return_date: datetime = datetime.strptime(year + day + string[-5:], '%Y-%m-%d %H:%M')

    return {
        'go_out_date': go_out_date,
        'return_date': return_date
    }


def datetime_to_str(go_out_date: datetime, return_date: datetime) -> str:
    go_out_date: str = datetime.strftime(go_out_date, "%m-%d %H:%M")
    return_date: str = datetime.strftime(return_date, "%H:%M")

    return go_out_date + ' ~ ' + return_date


class GoingOutApplyModel(db.Model, BaseMixin):
    __tablename__ = 'goingout'
    id: int = db.Column(db.Integer, primary_key=True)
    student_id: str = db.Column(db.String(20), db.ForeignKey('student.id', ondelete='CASCADE'))
    go_out_date: datetime = db.Column(db.DateTime)
    return_date: datetime = db.Column(db.DateTime)
    reason: str = db.Column(db.String(100))
    # 0: 외출 전. 1: 외출 중, 2: 복귀 완료
    goingout_status: int = db.Column(db.Integer, default=0)

    def __init__(self, student_id: str, go_out_date: datetime, return_date: datetime, reason: str):
        self.student_id = student_id
        self.go_out_date = go_out_date
        self.return_date = return_date
        self.reason = reason

    @staticmethod
    def check_going_out_apply_time(now: datetime, go_out_date: datetime, return_date: datetime):
        if (now.weekday() in {4, 5}) and (now.hour >= 22 and now.minute >= 30):
            if now.date() + timedelta(days=1) == go_out_date.date():
                raise ApplyTimeException

        if go_out_date.date() != return_date.date():
            raise ApplyTimeException

        difference_time = go_out_date - now
        if not difference_time <= timedelta(days=7):
            raise ApplyTimeException

    @staticmethod
    def get_going_out_apply(student_id: str) -> dict:
        applies: List['GoingOutApplyModel'] = GoingOutApplyModel.query.filter(
            GoingOutApplyModel.student_id == student_id,
            GoingOutApplyModel.return_date > datetime.now()
        ).all()

        if not applies:
            raise NoContentException

        going_out_data = {
            'workday': [],
            'saturday': [],
            'sunday': []
        }

        for apply in applies:
            days_of_week = apply.go_out_date.weekday()

            date = datetime_to_str(apply.go_out_date, apply.return_date)

            apply = {
                'date': date,
                'id': apply.id,
                'reason': apply.reason,
                'goingoutStatus': going_out_status_message[apply.goingout_status]
            }

            if days_of_week <= 4:
                going_out_data['workday'].append(apply)

            elif days_of_week == 5:
                going_out_data['saturday'].append(apply)

            else:
                going_out_data['sunday'].append(apply)

        return going_out_data

    @staticmethod
    def post_going_out_apply(student_id: str, date: str, reason: str):
        now = GoingOutApplyModel.kst_now()

        date_dict = str_to_datetime(date)
        go_out_date: datetime = date_dict.get('go_out_date')
        return_date: datetime = date_dict.get('return_date')

        GoingOutApplyModel.check_going_out_apply_time(now, go_out_date, return_date)
        GoingOutApplyModel(student_id, go_out_date, return_date, reason).save()

    @staticmethod
    def patch_going_out_apply(apply_id: int, student_id: str, date: str, reason: str):
        now = GoingOutApplyModel.kst_now()
        apply: 'GoingOutApplyModel' = GoingOutApplyModel.query.filter_by(id=apply_id, student_id=student_id).first()

        date_dict = str_to_datetime(date)
        go_out_date = date_dict.get('go_out_date')
        return_date = date_dict.get('return_date')

        GoingOutApplyModel.check_going_out_apply_time(now, go_out_date, return_date)
        apply.go_out_date = go_out_date
        apply.return_date = return_date
        apply.reason = reason

        db.session.commit()

    @staticmethod
    def delete_going_out_apply(apply_id: int, student_id: str):
        apply: 'GoingOutApplyModel' = GoingOutApplyModel.query.filter_by(id=apply_id, student_id=student_id).first()

        if apply is None:
            raise NoContentException()
        apply.delete()
