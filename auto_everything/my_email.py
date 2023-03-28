from typing import Any, Callable
import re
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


if __name__ == '__main__':
    def handle_email(from_id: str, from_: str, to: list[str], message: str):
        print(from_)
        print(to)
        print(message)

    smtp_service = SMTP_Service(
        host="0.0.0.0",
        port=25,
        handler=handle_email
    )

    # smtp_service.start()

    from_email = "ddsd@protonmail.com"
    result = SMTP_Service.get_authorized_ip_list_from_an_email_domain(from_email)
    if (len(result) > 0):
        an_ip = result[0].split("/")[0]
        ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip=an_ip)
        print(ok)
        ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip="127.0.0.1")
        print(ok)
        ok = SMTP_Service.check_if_an_email_was_sent_from_a_domain(email_address=from_email, source_ip=an_ip)
        print(ok)