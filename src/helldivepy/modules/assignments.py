import httpx

from helldivepy.models import Assignment
from helldivepy.modules import BaseModule


class AssignmentsModule(BaseModule):
    def get_all(self) -> list[Assignment]:
        data = self._get("/v1/assignments")
        return [Assignment.model_validate(assignment) for assignment in data]

    def get(self, index: int) -> Assignment | None:
        try:
            return Assignment.model_validate(self._get(f"/v1/assignments/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
