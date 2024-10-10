import logging
import requests
from requests.adapters import HTTPAdapter, Retry
from diveharder.constants import OFFICIAL_DIVEHARDER_URL, OFFICIAL_COMMUNITY_URL
from diveharder.models import APIURLConfiguration
import typing


def retry_adapter(
    backoff_factor: float, retries: int, extra_retry_codes: list = []
) -> HTTPAdapter:
    """Configures an HTTP adapter with retries and backoff."""
    retry_codes = [429] + extra_retry_codes
    retry_strategy = Retry(
        total=retries,
        status_forcelist=retry_codes,
        backoff_factor=backoff_factor,
        allowed_methods=["GET"],
    )
    return HTTPAdapter(max_retries=retry_strategy)


def set_logger(debug: bool) -> logging.Logger:
    """Configures debug logging if requested."""
    from rich.logging import RichHandler

    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    if debug:
        logger.addHandler(
            RichHandler(
                level=logging.DEBUG,
                omit_repeated_times=False,
                markup=True,
                rich_tracebacks=True,
                log_time_format="%X %p",
            )
        )
    return logger


class ApiClient:
    """
    The client used to interact with the Helldivers 2 APIs
    """

    _instance = None

    def __new__(cls, *args, **kwargs) -> typing.Self:
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    @classmethod
    def get_client(cls):
        return cls._instance

    def __init__(
        self,
        user_agent: str,
        user_contact: str,
        debug: bool = False,
        diveharder_url: str = OFFICIAL_DIVEHARDER_URL,
        community_url: str = OFFICIAL_COMMUNITY_URL,
    ) -> None:
        """The client used to interact with the Helldivers 2 APIs

        Args:
            user_agent (str): The user agent to use when making requests.
            user_contact (str): The user contact to use when making requests.
            debug (bool, optional): Enables debug logging for development.
            diveharder_url (str, optional): The diveharder API url to use. Defaults to `constants.OFFICIAL_DIVEHARDER_URL`.
            community_url (str, optional): The community API url to use. Defaults to `constants.OFFICIAL_COMMUNITY_URL`.
        """
        self.debug = debug
        self.logger = set_logger(debug)
        self.api_config = APIURLConfiguration(
            diveharder=diveharder_url, community=community_url
        )
        self._user_contact = user_contact
        self._user_agent = user_agent
        self._setup_session()

    def _setup_session(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self._user_agent,
                "X-Super-Client": self._user_agent,
                "X-Super-Contact": self._user_contact,
            }
        )
        self.session.mount("https://", retry_adapter(0.2, 5))
        if self.debug:
            self.session.mount("http://", retry_adapter(0.2, 5))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.api_config})"
