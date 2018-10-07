from app.docs import JWT_ACCESS_TOKEN

EXTENSION_GET = {
    'tags': ['Apply Extension'],
    'description': '학생 자신의 연장신청 정보를 조회합니다.',
    'parameters': [JWT_ACCESS_TOKEN],
    'responses': {
        '200': {
            'description': '연장신청 정보 조회 성공',
            'examples': {
                '': {
                    'classNum': 1,
                    'seatNum': 16
                }
            }
        },
        '204': {
            'description': '연장신청 정보 없음'
        },
        '403': {
            'description': '권한 없음'
        }
    }
}

EXTENSION_POST = {
    'tags': ['Apply Extension'],
    'description': '''연장신청
    11시 연장 신청 가능 시간: 17:30 - 20:30
    12시 연장 신청 가능 시간: 17:30 - 22:00
    ''',
    'parameters': [
        JWT_ACCESS_TOKEN,
        {
            'name': 'classNum',
            'description': '''
            연장 학습실 번호
            1: 가온실
            2: 나온실
            3: 다온실
            4: 라온실
            5: 3층 독서실
            6: 4층 독서실
            7: 5층 열린교실
            ''',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'seatNum',
            'description': '연장 학습실 자리 번호',
            'in': 'json',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '연장신청 성공'
        },
        '204': {
            'description': '연장신청 실패(신청 가능 시간 아님)'
        },
        '400': {
            'description': '이미 신청된 자리거나, 신청할 수 없는 곳(범위를 넘어섬)'
        },
        '403': {
            'description': '권한 없음'
        }
    }
}

EXTENSION_DELETE = {
    'tags': ['Apply Extension'],
    'description': '''연장 신청을 취소합니다.
    
    11시 연장 신청 취소 가능 시간: 17:30 - 20:30
    12시 연장 신청 취소 가능 시간: 17:30 - 22:00
    ''',
    'parameters': [JWT_ACCESS_TOKEN],
    'responses': {
        '200': {
            'description': '연장신청 취소 성공'
        },
        '204': {
            'description': '연장신청 취소 실패(취소 가능 시간 아님)'
        },
        '403': {
            'description': '권한 없음'
        }
    }
}

EXTENSION_MAP_GET = {
    'tags': ['Apply Extension'],
    'description': '연장신청 지도를 조회합니다. 해당 class에 대한 신청 여부, 신청되어 있다면 자리까지 response합니다. 신청되어 있지 않으면 자리는 0입니다.',
    'parameters': [
        JWT_ACCESS_TOKEN,
        {
            'name': 'classNum',
            'description': '지도를 조회할 학습실 번호',
            'in': 'query',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '지도 조회 성공',
            'examples': {
                '': {
                    'map': [
                        [1, 1, 1, 1, 1],
                        [1, 2, 0, 3, 4],
                        [5, 6, 0, '조민규', 8],
                        [9, 10, 0, 11, 12],
                        [13, 14, 0, 15, 16],
                        [17, 18, 0, 19, 20]
                    ],
                    'appliedThisClass': True,
                    'appliedSeat': 7
                }
            }
        },
        '403': {
            'description': '권한 없음'
        }
    }
}