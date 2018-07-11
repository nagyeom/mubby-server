class ClientInfo:
    def __init__(self, client_info):
        """
            Client info Class

                1. Default socket checking
                    - def socket_check(self): bool

                2. self.__client_info Updating
                    - def update_client_info(self, dict): void

                3. self.__client_info value Getting
                    - def get_client_info(self): dict

                4. self.__client_info[key] value Setting or Getting
                    - def __setitem__(self, key, value): void
                            < using outside > instance_name[key] = value

                    - def __getitem__(self, key): dict[key]
                            < using outside > instance_name[key]
        """

        self.__client_info = dict()
        """ YOU HAVE TO SET THE FOLLOWING VALUES """
        # """
        #     self.__client_info[request_socket_from_client]
        #     self.__client_info[alarm_socket_to_client]
        #     self.__client_info[stt_text]
        #     self.__client_info[tts_speech]
        #     self.__client_info[watson_context]
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

    def __getitem__(self, key):
        return self.__client_info[key]
