from typing import Literal

from pydantic import BaseModel, Field, model_validator

from google.adk.events import RequestInput


class ModelValidator(BaseModel):

    report_id: str

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


def ask_comment():
    
    yield RequestInput(
       message = "Rivedi la bozza generata e lascia un commento:",
       response_schema=ModelValidator
        
        
    )
""" decision = ModelValidator.model_validate({
    "report_id": "abc123",
    "decision": "request_revision",
    "comment": "Expand the analysis of Scope 3 emissions."
})

print(decision.decision) """