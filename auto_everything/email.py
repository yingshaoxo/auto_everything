from O365 import Account

class MyO365():
    def __init__(self, credentials):
        """
        credentials = ('dhasldl-b8ab-4730-93f1-cee730a4044b', 'salhdlghsaldh~ufOj2-4~69sCMZ05D_')
        """
        self.account = Account(credentials)
        ok = False
        if not self.account.is_authenticated:
            ok = self.account.authenticate(scopes=['basic', 'message_all'])
        else:
            ok = True
        if ok:
            print('Authenticated!')
        else:
            print('Not Authenticated!')
            raise Exception("Email sender not authenticated!")

    def send_email(self, receiver: str, subject: str, body: str):
        m = self.account.new_message()
        m.to.add(receiver)
        m.subject = subject
        m.body = body
        m.send()
