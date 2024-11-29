from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from decouple import config
import smtplib
import logging

logger = logging.getLogger(__name__)


class EmailNotificationManager:
    SMTP_SERVER = config("ITS_SMTP_SERVER")
    SMTP_PORT = config("ITS_SMTP_PORT")
    SENDER_EMAIL = config("ITS_EMAIL_ACCOUNT")
    SENDER_PASSWORD = config("ITS_EMAIL_PASSWORD")

    def _send_email(self, recipient, subject, html_body):
        try:
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()
            server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)

            msg = MIMEMultipart("alternative")
            msg["From"] = self.SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(self.SENDER_EMAIL, recipient, msg.as_string())
            logger.info(f"Email sent to {recipient}")

        except Exception as e:
            logger.error(f"An error occurred while sending the email: {e}")

        finally:
            server.quit()

    def _load_template(self, template_path):
        try:
            with open(template_path) as file:
                return Template(file.read())
        except Exception as e:
            logger.error(f"An error occurred while loading the template: {e}")
            raise

    def send_verification_email(self, recipient, code):
        template = self._load_template(
            "asyncjobs/assets/html/recovery-password.html")
        html_body = template.substitute(code=code)
        self._send_email(
            recipient, "Verification Code - ITS RFC APP", html_body)

    def send_certificates_request_email(self, recipients, data):
        template = self._load_template(
            "asyncjobs/assets/html/certificate-request.html")
        certificates_html = "".join(
            f"<li>{cert}</li>" for cert in data["certificates"])
        html_body = template.substitute(
            id=data["id"],
            concessionaire=data["concessionaire"],
            user=data["user"],
            created_at=data["created_at"],
            has_support_files=str(data["has_support_files"]),
            request_type=data["request_type"],
            status=data["status"],
            description=data["description"],
            environment=data["environment"],
            has_service_account=str(data["has_service_account"]),
            certificates_list=certificates_html,
            front_url=config("ITS_FRONTEND_URL"),
        )
        for recipient in recipients:
            self._send_email(
                recipient, "Request Details - ITS RFC APP", html_body)

    def send_firmware_request_email(self, recipients, data):
        template = self._load_template(
            "asyncjobs/assets/html/firmware-request.html")
        buses = data["config_file"].get("buses", [])
        buses_list = "".join(f"<li>{bus}</li>" for bus in buses)
        buses_section = f"<h3>Buses</h3><ul>{buses_list}</ul>" if buses else ""
        html_body = template.substitute(
            id=data["id"],
            created_at=data["created_at"],
            environment=data["config_type"],
            concessionaire=data["concessionaire"],
            status=data["status"],
            description=data["description"],
            request_type=data["request_type"],
            config_type=data["config_type"],
            filename=data["config_file"]["filename"],
            version=data["config_file"]["version"],
            time=data["config_file"]["time"],
            date=data["config_file"]["date"],
            buses_section=buses_section,
            front_url=config("ITS_FRONTEND_URL"),
        )
        for recipient in recipients:
            self._send_email(
                recipient, "Request Details - ITS RFC APP", html_body)
