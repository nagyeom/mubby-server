# -*- coding:utf-8 -*-

import json
import os


class WatsonServer:
    def __init__(self):
        # 환경변수가 설정 안 되어있을 때도 에러를 반환해야한다.

        # client 마다 객체에 context 를 넣었다가 호출해야하는 것은 아닐까?
        # 대화가 이어지기 위해서는 이전의 context 값이 필요하다.
        # Aibril 에 접근하기 위해서는 watson id 가 필요하다.
        self.watson_username = os.getenv('watson_username')
        self.watson_password = os.getenv('watson_password')
        self.watson_workspace = os.getenv('watson_workspace')
        self.watson_url = os.getenv('watson_url')
        self.watson_version = os.getenv('watson_version')

        self.context = {'timezone': 'Asia/Seoul'}
        self.watson_conv_id = ''
        self.conversation = None
        self.aibril_conv_connect()

        print("Watson Server make")

    def aibril_conv_connect(self):
        try:
            self.conversation = conversation_v1.ConversationV1(
                username=self.watson_username,
                password=self.watson_password,
                version=self.watson_version,
                url=self.watson_url
            )

            # response 함수 화 할 것 그 이후 동작도 함수화 해서 분리할 것.
            response = self.conversation.message(
                workspace_id=self.watson_workspace,
                # message_input 을 여기다 안 해줘도 상관없지 않나?
                # context 도 connection 부분에서는 사용하는게 현재로는 없어 보인다.
                message_input={'text': ''},
                context=self.context
            )
            self.watson_conv_id = response['context']['conversation_id']
            self.context['conversation_id'] = self.watson_conv_id

        except Exception as e:
            # self.logger.write_critical("cannot connect Aibril conversation server!!!")
            return "에이브릴 대화서버에 접속 할 수 없습니다."

    def aibril_conv(self, text):
        print("text >> {}".format(text))
        if self.watson_conv_id == '':
            self.aibril_conv_connect()

        response = self.conversation.message(
            workspace_id=self.watson_workspace,
            message_input={'text': text},
            context=self.context
        )

        print("response >> {}".format(response))

        # response type 출력 해볼 것, json parsing 이 딱히 필요 없을 수도
        json_response = json.dumps(response, indent=2, ensure_ascii=False)
        dict_response = json.loads(json_response)

        # ==================================================
        #   Debug response print
        # ==================================================
        # self.logger.write_debug(dict_response)

        try:
            # ==================================================
            #   Parsing response
            # 얘만 따로 try, catch 로 감싸서 text 가 없는 경우에도 대비해야 한다.
            # 답이 없을 수도 있다. header 를 먼저 받아와야 한다.
            # header > text > language 순으로 정의해야한다.
            # ==================================================
            result_conv = dict_response['output']['text'][0]
            # check this action
            # 다음 문장 추가해서 읽는 것 같은데, 이건 왜 하는 건가?
            # 아래 두 줄은 없어도 동작이 잘 되었었다.
            # 여러개의 문장을 읽어와서 연결하도록 하기 위해 사용 하는 것 같다.
            if len(dict_response['output']['text']) > 1:
                result_conv += " " + dict_response['output']['text'][1]
        except Exception as e:
            print('\n\t error >> '.format(e))
            result_conv = "다시 한번 말씀해주세요."

        try:
            header = dict_response['output']['header']
            print('header type {}'.format(type(header)))
        except Exception as e:
            header = {"command": "chat"}
            print("It dosen't have Header >> {}".format(e))

            # ==================================================
            #   Update context
            # context 안에 변수 넣어서 에이브릴에서 사용하게 할 수 있음.
            # 딕셔너리 value 안에 리스트 혹은 딕셔너리로 사용.
            # 사용 후에 value 삭제 후  update.
            # ==================================================
            self.context.update(dict_response['context'])

            # test 용
            # self.context["dir"] = {"aa":"I_am_Leni", "bb":"2"}

            # ==================================================
            #   Check conversation is end or durable
            # ==================================================
            if 'branch_exited' in dict_response['context']['system']:
                conv_flag = True
            else:
                conv_flag = False

            # --------------------------------------------------
            #   << Check Translate >>
            # 언어 설정하는 부분인데, 현재는 통역이 안되서 그냥 반환만 하고 있음.
        try:
            language = (result_conv.split())[-1]
        except Exception as e:
            language = 'trans_ko'
            print("It dosen't have Text >> {}".format(e))

        if language == 'trans_en':
            language = 'en'
        elif language == 'trans_ja':
            language = 'ja'
        elif language == 'trans_zh':
            language = 'zh'
        else:
            language = 'ko'
        # --------------------------------------------------

        print("return")
        return header, result_conv, language


# aibril_connector.py 만 동작해서 Aibril 대화셋 동작을 확인 할 수 있다.
if __name__ == "__main__":
    aibril = WatsonServer()
    text = '안녕'
    while True:
        header, text, language = aibril.aibril_conv(text)
        print('header >> {}\ntext >> {}\nlanguage >> {}'.format(header, text, language))
        text = input('\n\t 입력 >> ')
        if text == '종료':
            break