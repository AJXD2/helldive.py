import logging
import requests
from requests.adapters import HTTPAdapter, Retry
from helldivepy.constants import OFFICIAL_DIVEHARDER_URL, OFFICIAL_COMMUNITY_URL
import helldivepy.models as models
import typing
import helldivepy.api as modules


def retry_adapter(
    backoff_factor: float, retries: int, extra_retry_codes: list | None = None
) -> HTTPAdapter:
    """Configures an HTTP adapter with retries and backoff."""
    if extra_retry_codes is None:
        extra_retry_codes = []
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
    logger.level = logging.DEBUG if debug else 5000
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


class ModuleDict(typing.TypedDict):
    """A dictionary of modules."""

    war: modules.WarModule
    dispatch: modules.DispatchModule
    steam: modules.SteamModule
    assignments: modules.AssignmentsModule
    planets: modules.PlanetsModule
    campaigns: modules.CampaignModule


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
        self.api_config = models.APIURLConfiguration(
            diveharder=diveharder_url, community=community_url
        )
        self._user_contact = user_contact
        self._user_agent = user_agent
        self._setup_session()
        self._modules = ModuleDict(
            war=modules.WarModule(self),
            dispatch=modules.DispatchModule(self),
            steam=modules.SteamModule(self),
            assignments=modules.AssignmentsModule(self),
            planets=modules.PlanetsModule(self),
            campaigns=modules.CampaignModule(self),
        )

    def _setup_session(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self._user_agent,
                "X-Super-Client": self._user_agent,
                "X-Super-Contact": self._user_contact,
            }
        )
        self.session.mount("https://", retry_adapter(0.2, 2))
        self.session.mount("http://", retry_adapter(0.2, 2))

    def get_war_info(self) -> models.WarInfo:
        return self._modules["war"].get_war_info()

    # ==============[Modules]==============

    @property
    def war(self) -> modules.WarModule:
        return self._modules["war"]

    @property
    def dispatch(self) -> modules.DispatchModule:
        return self._modules["dispatch"]

    @property
    def steam(self) -> modules.SteamModule:
        return self._modules["steam"]

    @property
    def assignments(self) -> modules.AssignmentsModule:
        return self._modules["assignments"]

    @property
    def major_orders(self) -> modules.AssignmentsModule:
        return self.assignments

    @property
    def planets(self) -> modules.PlanetsModule:
        return self._modules["planets"]

    @property
    def campaigns(self) -> modules.CampaignModule:
        return self._modules["campaigns"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.api_config})"
