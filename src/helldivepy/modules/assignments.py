import httpx

from helldivepy.models import Assignment
from helldivepy.modules import BaseModule


class AssignmentsModule(BaseModule):
    """Access Major Orders (assignments) issued by high command."""

    def get_all(self) -> list[Assignment]:
        """Fetch all active assignments.

        Returns:
            A list of all currently active Major Orders.
        """
        data = self._get("/v1/assignments")
        return [Assignment.model_validate(assignment) for assignment in data]

    def get(self, index: int) -> Assignment | None:
        """Fetch a specific assignment by ID.

        Args:
            index: The assignment ID.

        Returns:
            The matching Assignment, or None if not found.
        """
        try:
            return Assignment.model_validate(self._get(f"/v1/assignments/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
