from typing import Dict

from constants import MAIL_TEMPLATE_CATEGORY, URL_CONTENT_TYPE


class MailBuilder:
    """Mail Builder"""

    def __init__(self) -> None:
        pass

    def build_template(self, content_type: str = "", **kwargs: Dict[str, int]) -> str:
        """method to build the email template

        Args:
            content_type (str): type of the template to choose from
            kwargs: contains the data for embedding in template. key should be matched
            with keys in the template
        Returns:
            str: generated template
        """
        if content_type == MAIL_TEMPLATE_CATEGORY[URL_CONTENT_TYPE]:
            mail_template = self._url_share_template(**kwargs)
        else:
            mail_template = self._mail_template(**kwargs)
        return mail_template

    @staticmethod
    def _url_share_template(**kwargs) -> str:
        """Return the url sharing template
        Args:
            kwargs: must contain the url
        Returns:
            str: template
        """
        template = f"""
        Dear User,

        Please find the generated report url:

        Report URL: {kwargs.get("content", "")}

        Best regards,
        The Team
        """
        return template

    @staticmethod
    def _mail_template(**kwargs) -> str:
        """Return the mail template
        Args:
            kwargs: content
        Returns:
            str: template
        """
        template = f"""
        Dear User,

        {kwargs.get("content", "")}

        Best regards,
        The Team
        """
        return template
