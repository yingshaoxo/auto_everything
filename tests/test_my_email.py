from auto_everything.my_email import SMTP_Service

def test_my_email():
    # def handle_email(from_id: str, from_: str, to: str, message: str):
    #     print(from_)
    #     print(to)
    #     print(message)

    # smtp_service = SMTP_Service(
    #     host="0.0.0.0",
    #     port=25,
    #     handler=handle_email
    # )

    # # smtp_service.start()

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