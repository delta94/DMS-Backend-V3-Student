from app.doc import JWT_ACCESS_TOKEN, parameter


CHANGE_PW_PATCH = {
    'tags': ['Account'],
    'description': '비밀번호 변경',
    'parameters': [
        JWT_ACCESS_TOKEN,
        {
            'name': 'currentPassword',
            'description': '현재 비밀번호',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'newPassword',
            'description': '바꿀 비밀번호',
            'in': 'json',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '비밀번호 변경 성공'
        },
        '205': {
            'description': '현재 비밀번호와 새 비밀번호가 동일함'
        },
        '403': {
            'description': '비밀번호 변경 실패(틀린 비밀번호), 또는 권한 없음'
        }
    }
}

FIND_PW_POST = {
    'tags': ['Account'],
    'description': '''비밀번호 초기화
    
    이메일발송 후 이메일 링크 클릭시 1234로 초기화''',
    'parameters': [
        parameter('id', '아이디'),
        parameter('email', '학교 이메일'),
    ],
    'responses': {
        '201': {
            'description': '이메일 발송 성공'
        },
        '204': {
            'description': '없는 아이디'
        },
        '205': {
            'description': '아이디에 이메일이 맞지 않음'
        }
    }
}
