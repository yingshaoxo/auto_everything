from typing import Any, Callable
import re


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
    def __init__(self, host: str, port: int, handler: Callable[[str, str, str], None]):
        """
        host: 0.0.0.0
        port: 25
        handler: (from: str, to: str, content: str) => None
        """
        from aiosmtpd.controller import Controller

        class CustomHandler:
            async def handle_DATA(self, server: Any, session: Any, envelope: Any):
                mail_from = envelope.mail_from
                mail_to = envelope.rcpt_tos
                data = envelope.content

                try:
                    print(f"mail_from: {mail_from}")
                    print("\n\n---\n\n")
                    handler(mail_from, mail_to, data.decode(encoding="utf-8"))
                except Exception as e:
                    print(e)
                    return '500 Could not process your message'

                return '250 OK'
        
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


if __name__ == '__main__':
    def handle_email(from_: str, to: str, message: str):
        print(from_)
        print(to)
        print(message)

    smtp_service = SMTP_Service(
        host="0.0.0.0",
        port=25,
        handler=handle_email
    )

    smtp_service.start()