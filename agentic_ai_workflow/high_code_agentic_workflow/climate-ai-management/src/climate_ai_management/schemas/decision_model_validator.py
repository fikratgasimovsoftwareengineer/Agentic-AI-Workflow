from typing import Literal

from pydantic import BaseModel, Field, model_validator



class ModelValidator(BaseModel):

    decision: Literal[
        "approve",
        "reject",
        "request_revision"
    ]

    comment: str = Field(default="")

    @model_validator(mode="after")
    def validate_review(self):

        if (
            self.decision == "request_revision"
            and not self.comment.strip()
        ):
            raise ValueError(
                "Revision feedback is required."
            )

        return self


""" decision = ModelValidator.model_validate({
    "report_id": "abc123",
    "decision": "request_revision",
    "comment": "Expand the analysis of Scope 3 emissions."
})

print(decision.decision) """