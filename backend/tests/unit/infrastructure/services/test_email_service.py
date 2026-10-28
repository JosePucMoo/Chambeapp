from email import message_from_string
from email.header import decode_header, make_header

import pytest

from infrastructure.services.email_service import SmtpEmailSender


def decoded_body(raw_message: str) -> str:
    message = message_from_string(raw_message)
    parts = []
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type().startswith("text/"):
                payload = part.get_payload(decode=True)
                if payload:
                    parts.append(payload.decode(part.get_content_charset() or "utf-8"))
    else:
        payload = message.get_payload(decode=True)
        if payload:
            parts.append(payload.decode(message.get_content_charset() or "utf-8"))
    return "\n".join(parts)


def subject_of(raw_message: str) -> str:
    message = message_from_string(raw_message)
    return str(make_header(decode_header(message["Subject"])))


class FakeSMTP:
    instances = []

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.started_tls = False
        self.logged_in = None
        self.sent = []
        FakeSMTP.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        self.started_tls = True

    def login(self, username, password):
        self.logged_in = (username, password)

    def sendmail(self, from_email, to_email, message):
        self.sent.append((from_email, to_email, message))


class ExplodingSMTP:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        raise OSError("connection refused")

    def __exit__(self, *args):
        return False


@pytest.fixture(autouse=True)
def reset_fake_smtp():
    FakeSMTP.instances.clear()
    yield
    FakeSMTP.instances.clear()


@pytest.fixture
def email_sender(monkeypatch) -> SmtpEmailSender:
    monkeypatch.setenv("FRONTEND_URL", "https://app.test")
    monkeypatch.setattr("infrastructure.services.email_service.smtplib.SMTP", FakeSMTP)
    return SmtpEmailSender(
        host="smtp.test", port=587, username="user", password="pass", from_email="no-reply@test.com"
    )


class TestSmtpEmailSender:
    def test_send_verification_email(self, email_sender: SmtpEmailSender):
        email_sender.send_verification_email(
            to_email="invitee@test.com", verification_token="token-1"
        )

        server = FakeSMTP.instances[0]
        assert server.started_tls is True
        assert server.logged_in == ("user", "pass")

        from_email, to_email, message = server.sent[0]
        assert from_email == "no-reply@test.com"
        assert to_email == "invitee@test.com"
        body = decoded_body(message)
        assert subject_of(message) == "Verifica tu cuenta en Chambeapp"
        assert "https://app.test/auth/verify-account/token-1" in body
        assert "activar tu cuenta" in body

    def test_send_password_reset_email(self, email_sender: SmtpEmailSender):
        email_sender.send_password_reset_email(
            to_email="invitee@test.com", verification_token="token-2"
        )

        _, to_email, message = FakeSMTP.instances[0].sent[0]
        body = decoded_body(message)
        assert to_email == "invitee@test.com"
        assert subject_of(message) == "Restablecer contraseña en Chambeapp"
        assert "https://app.test/auth/reset-password/token-2" in body
        assert "contraseña" in body

    def test_send_project_invitation_email(self, email_sender: SmtpEmailSender):
        email_sender.send_project_invitation_email(
            to_email="invitee@test.com",
            verification_token="token-3",
            sender_name="Owner",
            project_title="Project",
        )

        _, to_email, message = FakeSMTP.instances[0].sent[0]
        body = decoded_body(message)
        assert to_email == "invitee@test.com"
        assert subject_of(message) == "Invitación de proyecto"
        assert "https://app.test/invitations/token-3" in body
        assert "Project" in body
        assert "Owner" in body

    def test_smtp_failure_is_logged_and_not_propagated(self, monkeypatch):
        monkeypatch.setenv("FRONTEND_URL", "https://app.test")
        monkeypatch.setattr("infrastructure.services.email_service.smtplib.SMTP", ExplodingSMTP)
        sender = SmtpEmailSender(
            host="smtp.test",
            port=587,
            username="user",
            password="pass",
            from_email="no-reply@test.com",
        )

        sender.send_verification_email(to_email="invitee@test.com", verification_token="token-1")
