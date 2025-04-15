import asyncio
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    Cc,
)

from constants.http_status_codes import HTTP_550_MAILBOX_UNAVAILABLE, HTTP_200_OK
from src.entities.config.config_entity import MailConfig


class SendGridManager:
    """
    A class for sending emails for Prognosis related services using Sendgrid.

    """

    def __init__(self, mail_config: MailConfig) -> None:
        """
        Initialize a Manger to handle email functionalities
        """
        self.mail_config = mail_config
        # Initialize the connection
        self.connection = SendGridAPIClient(api_key=self.mail_config.sendgrid_api_key)

    def sendmail(
        self,
        receiver: list,
        subject: str,
        body: str = None,
        html_body: str = None,
        cc=None,
        bcc=None,
        attachments=None,
    ) -> dict:
        """
        Send an email synchronously.

        Args:
            receiver (list): List of recipient email addresses.
            body (str, optional): Email template. Defaults to None (uses self.template).
            subject(str): Email subject
            cc (list): List of CC (carbon copy) email addresses.
            bcc (list): List of BCC (blind carbon copy) email addresses.
            attachments: attachments details

        Returns:
            bool: True if the email is sent successfully, False otherwise.
        """
        if not receiver:
            raise ValueError("Recipient address is missing.")

        cc = cc if cc else []
        bcc = bcc if bcc else []

        # Create a Sendgrid Mail Object
        message = Mail(
            from_email=self.mail_config.sendgrid_host_user,
            # bcc = bcc,
            to_emails=receiver,
            subject=subject,
            plain_text_content=body,
            html_content=html_body
        )
        for cc_email in cc:
            message.add_cc(Cc(cc_email))

        if attachments:
            attachment_content_base64 = base64.b64encode(attachments).decode("utf-8")
            attachment = Attachment(
                FileContent(attachment_content_base64),
                FileName("report.pdf"),
                FileType("application/pdf"),
                Disposition("attachment"),
            )
            message.add_attachment(attachment)

        try:
            self.connection.send(message)
            mail_response = {
                "message": "Email send successfully",
                "status": HTTP_200_OK
            }
            return mail_response
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            mail_response = {
                "message": "Sending mail failed. Please check your network or contact the admin.",
                "status": HTTP_550_MAILBOX_UNAVAILABLE
            }
            return mail_response

    async def sendmail_async(
        self, receiver: list, body: str, cc=None, bcc=None, attachments=None
    ):
        """
        Send an email asynchronously.

        Args:
            receiver (list): List of recipient email addresses.
            body (str, optional): Email template. Defaults to None (uses self.template).
            cc (list): List of CC email addresses.
            bcc (list): List of BCC email addresses.

        Returns:
            bool: True if the email is sent successfully, False otherwise.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.sendmail, receiver, body, cc, bcc, attachments
        )
