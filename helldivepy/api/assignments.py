from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class AssignmentsModule(BaseApiModule):
    """
    The Assignments API module (Major Order). This module is used to interact with the current major order(s).

    Methods:
        get_all_assignments(): Gets all current assignments
        get_assignment(assignment_id: int): Gets one assignment using the assignment ID

    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_all_assignments(self) -> typing.List[models.Assignment]:
        """
        Gets all current assignments
        """
        data = self.get("community", "api", "v1", "assignments")
        return [models.Assignment(**assignment) for assignment in data]

    def get_assignment(self, assignment_id: int) -> models.Assignment:
        """
        Gets one assignment using the assignment ID
        """
        data = self.get("community", "api", "v1", "assignments", str(assignment_id))
        return models.Assignment(**data)
