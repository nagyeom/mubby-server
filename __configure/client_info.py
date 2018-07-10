class ClientInfo:
    def __init__(self, client_info):
        """
            Client info Class

                1.
                2.
                3.

        """

        self.__client_info = dict()
        # """
        #     self.__client_info[request_socket_from_client]
        #     self.__client_info[alarm_socket_to_client]
        #     self.__client_info[stt_text]
        #     self.__client_info[tts_speech]
        #     self.__client_info[watson_content]
        #     self.__client_info[watson_response]
        # """

        self.update_client_info(client_info)

    def socket_check(self):
        """
            If you didn't have default sockets you couldn't start

            :return: void
        """
        is_success = True
        if not self.__client_info[request_socket_from_client]:
            print('You have to set request_socket from client')
            is_success = False
        if not self.__client_info[alarm_socket_to_client]:
            print('You have to set alarm_socket to client')
            is_success = False

        return is_success

    def update_client_info(self, client_info):
        self.__client_info = client_info

    def get_client_info(self):
        return self.__client_info

    def __setitem__(self, key, value):
        self.__client_info[key] = value

    def __getitem__(self, item):
        return self.__client_info[item]


if __name__ == "__main__":
    diccct = { 'request_socket_from_client': 'request_socket_from_client_test1', 'alarm_socket_to_client': 'alarm_socket_to_client_test1'}
    c = ClientInfo(diccct)
    print(c.get_client_info())
    c['request_socket_from_client'] = 'hi'
    print(c['request_socket_from_client'])