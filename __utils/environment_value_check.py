import os


def watson_environment():
    watson_key = ('watson_username', 'watson_password', 'watson_workspace', 'watson_url', 'watson_version')

    for key in watson_key:
        watson_value = os.getenv(key)
        if watson_value is not None:
            yield key, watson_value
        else:
            print('{} 환경변수 설정이 필요합니다.\n'.format(key))
            exit(1)


def google_environment():
    key = 'GOOGLE_APPLICATION_CREDENTIALS'
    google_value = os.getenv(key)
    if google_value is not None:
        return google_value
    else:
        print('{} 환경변수 설정이 필요합니다.\n'.format(key))
        exit(1)
