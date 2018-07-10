# Client Info
CLIENT = {
    'request_socket_from_client': '',
    'alarm_socket_to_client': '',
    'stt_text': '',
    'tts_speech': '',
    'watson_content': '',
    'watson_response': '',
}

# Client List
CLIENT_LIST = dict()

# Audio
EXTENSION = ".wav"

# Network
HOST = ''
REQUEST_PORT = 5555
ALARM_PORT = 5556
REQUEST_ADDR = (HOST, REQUEST_PORT)
ALARM_ADDR = (HOST, ALARM_PORT)

FILE_HEADER_SIZE = 44
FILE_READ_SIZE = 8192
BUF_SIZE = 1024