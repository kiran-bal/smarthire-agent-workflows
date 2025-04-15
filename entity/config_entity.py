from dataclasses import dataclass


@dataclass(frozen=True)
class AgentsConfig:
    """Agent Configuration Details
    """
    agent_category_config: dict
    agents_config: dict
    agent_tools_config: dict


@dataclass(frozen=True)
class MailConfig:
    """Mailer Configuration
    """
    sendgrid_api_key: str
    sendgrid_host_user: str


@dataclass(frozen=True)
class MessageConfig:
    """Message Configuration
    """
    twillio_url: str
    text_local_url: str
    timeout: int
