from dataclasses import dataclass
from typing import Any, Callable
import re
import asyncio

from auto_everything.network import Network
net_work = Network()


class MyO365():
    def __init__(self, credentials: tuple[str, str]):
        """
        credentials = ('dhasldl-b8ab-4730-93f1-cee730a4044b', 'salhdlghsaldh~ufOj2-4~69sCMZ05D_')
        """
        from O365 import Account
        self.account = Account(credentials)
        ok = False
        if not self.account.is_authenticated:
            ok = self.account.authenticate(scopes=['basic', 'message_all']) #type: ignore
        else:
            ok = True
        if ok:
            print('Authenticated!')
        else:
            print('Not Authenticated!')
            raise Exception("Email sender not authenticated!")

    def send_email(self, receiver: str, subject: str, body: str):
        m = self.account.new_message() #type: ignore
        m.to.add(receiver) #type: ignore
        m.subject = subject
        m.body = body
        m.send()


class SMTP_Service():
    domain_to_ip_list: dict[str, Any] = {}

    def __init__(self, host: str, port: int, handler: Callable[[str, str, list[str], str], None], auth_ip_source: bool = False):
        """
        host: 0.0.0.0
        port: 25
        handler: (from_ip: str, from: str, to: list[str], content: str) => None
        """
        from aiosmtpd.controller import Controller

        class CustomHandler:
            async def handle_DATA(self, server: Any, session: Any, envelope: Any):
                mail_from = envelope.mail_from
                mail_to = envelope.rcpt_tos
                data = envelope.content
                source_ip_address = session.peer[0]

                if (auth_ip_source == True):
                    ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=mail_from, source_ip=source_ip_address)
                    if not ok:
                        return

                try:
                    # print(f"mail_from: {mail_from}")
                    # print("\n\n---\n\n")
                    handler(source_ip_address, mail_from, mail_to, data.decode(encoding="utf-8"))
                except Exception as e:
                    print(e)
                    return '500 Could not process your message'

                return '250 OK'
        
        self.auth_ip_source = auth_ip_source
        self.host = host
        self.port = port
        self.custom_handler = CustomHandler()
        self.controller = Controller(self.custom_handler, hostname=host, port=port)

    def start(self):
        from time import sleep
        self.controller.start()
        print(f'SMTP server is running on {self.host}:{self.port}.\n\n')
        while True:
            sleep(5)
    
    def stop(self):
        self.controller.stop()
    
    @staticmethod
    def get_title_from_email_string_data(data: str) -> None | str:
        title_list = re.findall(r"Subject:\s+(.*)", data, re.IGNORECASE)
        if len(title_list) == 0:
            return None
        else:
            return title_list[0]
    
    @staticmethod
    def get_authorized_ip_list_from_an_email_domain(email_address: str) -> list[str]:
        default_result: list[str] = []

        base_domain = email_address
        if "@" in email_address:
            base_domain = email_address.split("@")[1].strip()
        
        if base_domain in SMTP_Service.domain_to_ip_list.keys():
            return SMTP_Service.domain_to_ip_list[base_domain]
        
        text_record_list = net_work.get_text_record_by_using_domain_url(url=base_domain)
        found = None
        for one_record in text_record_list:
            if "v=spf1" in one_record:
                found = one_record
                break
        
        if found != None:
            ipv4_list = re.findall(r"ip4:([\w\.\-\_\/]+)", found)
            if len(ipv4_list) > 0:
                return ipv4_list

            result: list[str] = []

            rediret_list = re.findall(r"redirect:([\w\.\-\_\/]+)", found)
            if len(rediret_list) > 0:
                result += SMTP_Service.get_authorized_ip_list_from_an_email_domain(email_address=rediret_list[0])

            include_list = re.findall(r"include:([\w\.\-\_\/]+)", found)
            for one in include_list:
                result += SMTP_Service.get_authorized_ip_list_from_an_email_domain(email_address=one)
            
            if len(result) > 0:
                SMTP_Service.domain_to_ip_list[base_domain] = result

            return result

        return default_result

    @staticmethod
    def check_if_an_email_was_sent_from_a_domain(email_address: str, source_ip: str) -> bool:
        network_or_ip_list = SMTP_Service.get_authorized_ip_list_from_an_email_domain(email_address=email_address)
        for one in network_or_ip_list:
            yes = net_work.check_if_an_ip_in_an_ip_network(ip=source_ip, ip_network=one)
            if yes:
                return True
        return False


@dataclass()
class My_Telegram_Message():
    from_chat_id: str | None = None
    from_user_id: str | None = None
    from_user_name: str | None = None
    text: str | None = None


class Telegram_Bot():
    def __init__(self, token: str):
        try:
            import telegram
            self.telegram = telegram
            self.bot: telegram.Bot = telegram.Bot(token)
            self.last_update_id = None
        except Exception as e:
            print(e)
            print(f"""
error: You should install python-telegram-bot by using:

python -m pip install python-telegram-bot
            """)
    
    def send_message(self, chat_id: str, text: str):
        async def send_message_function():
            async with self.bot:
                await self.bot.send_message(text=text, chat_id=int(chat_id)) #type: ignore
        loop = asyncio.get_event_loop()
        task = loop.create_task(send_message_function())
        loop.run_until_complete(task)
        
    async def get_new_message_updates(self):
        messages: list[self.telegram.Update] = []
        if self.last_update_id != None:
            messages = list(await self.bot.get_updates(offset=self.last_update_id+1, timeout=30)) #type: ignore
        else:
            messages = list(await self.bot.get_updates(timeout=30)) #type: ignore
        if len(messages) > 0:
            self.last_update_id = messages[-1].update_id
        return messages

    async def get_messages(self) -> list[My_Telegram_Message]:
        messages: list[My_Telegram_Message] = []
        updates = await self.get_new_message_updates()
        for update in updates:
            if update.message != None and update.message.from_user != None and update.message.from_user.username != None and update.message.text != None:
                """
                Message(channel_chat_created=False, chat=Chat(first_name='yingshao', id=131513300, last_name='xo', type=<ChatType.PRIVATE>, username='yingshaoxo'), date=datetime.datetime(2023, 3, 30, 9, 4, 23, tzinfo=<UTC>), delete_chat_photo=False, from_user=User(first_name='yingshao', id=131513300, is_bot=False, language_code='en', last_name='xo', username='yingshaoxo'), group_chat_created=False, message_id=1363, supergroup_chat_created=False, text='hi')
                """
                messages.append(My_Telegram_Message(
                    from_chat_id=str(update.message.chat.id),
                    from_user_id=str(update.message.from_user.id),
                    from_user_name=str(update.message.from_user.username),
                    text=str(update.message.text)
                ))
        return messages

    def get_message_loop(self, new_message_handler: Callable[[My_Telegram_Message], None], sleep_time_in_second: float = 1):
        """
        new_message_handler: (My_Telegram_Message) => None
            it is a function that handles new message, it will receive an object like this:
            ```
            @dataclass()
            class My_Telegram_Message():
                from_chat_id: str | None = None
                from_user_id: str | None = None
                from_user_name: str | None = None
                text: str | None = None
            ```
        """
        async def loop_function():
            while True:
                messages = await self.get_messages()
                for msg in messages:
                    try:
                        # print(msg)
                        new_message_handler(msg)
                    except Exception as e:
                        print(f"error: {e}")
                await asyncio.sleep(sleep_time_in_second)
        loop = asyncio.get_event_loop()
        task = loop.create_task(loop_function())
        loop.run_until_complete(task)
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # asyncio.ensure_future(loop_function())
        # loop.run_forever()


if __name__ == '__main__':
    # def handle_email(from_id: str, from_: str, to: list[str], message: str):
    #     print(from_)
    #     print(to)
    #     print(message)

    # smtp_service = SMTP_Service(
    #     host="0.0.0.0",
    #     port=25,
    #     handler=handle_email
    # )

    # # smtp_service.start()

    # from_email = "ddsd@protonmail.com"
    # result = SMTP_Service.get_authorized_ip_list_from_an_email_domain(from_email)
    # if (len(result) > 0):
    #     an_ip = result[0].split("/")[0]
    #     ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip=an_ip)
    #     print(ok)
    #     ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip="127.0.0.1")
    #     print(ok)
    #     ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip=an_ip)
    #     print(ok)

    # from auto_everything.my_email import Telegram_Bot
    # telegram_bot = Telegram_Bot(token="")

    # def message_handler(msg_object):
    #     print(msg_object.text)

    # if __name__ == '__main__':
    #     telegram_bot.get_message_loop(
    #         new_message_handler=message_handler
    #     )

    pass