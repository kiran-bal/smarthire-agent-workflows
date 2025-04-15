import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from crewai.tools import tool


class GmailTools:
    """Contains tools for sending emails via Gmail API."""

    # Gmail API scopes and file paths
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'credentials.json'

    @staticmethod
    def _get_gmail_service():
        """Authenticates and returns a Gmail service instance."""
        creds = None
        if os.path.exists(GmailTools.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(GmailTools.TOKEN_FILE, GmailTools.SCOPES)

        # Refresh or create new credentials if expired/missing
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GmailTools.CREDENTIALS_FILE, GmailTools.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the new token
            with open(GmailTools.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    @staticmethod
    @tool("Send an email via Gmail")
    def send_email(to_email: str, subject: str, body: str) -> str:
        """
        Sends an email using Gmail API. Requires OAuth2 authentication (credentials.json and token.json).

        Args:
            to_email (str): Recipient email address.
            subject (str): Email subject.
            body (str): Email body content.

        Returns:
            str: Success/failure message.
        """
        try:
            service = GmailTools._get_gmail_service()
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            send_message = service.users().messages().send(
                userId="me",
                body={'raw': raw_message}
            ).execute()

            return f"Email sent to {to_email} (Message ID: {send_message['id']})"

        except Exception as e:
            return f"Failed to send email: {str(e)}"


def gmail_send_tool():
    """Returns the Gmail send_email tool for CrewAI."""
    return GmailTools.send_email