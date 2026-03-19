from helldivepy.models import War

from . import BaseModule


class WarModule(BaseModule):
    """Access the global war state."""

    def get(self) -> War:
        """Fetch the current war status snapshot.

        Returns:
            The current War state including statistics and active factions.
        """
        return War.model_validate(self._get("/v1/war"))
