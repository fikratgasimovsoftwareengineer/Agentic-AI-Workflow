from typing import Type
from pydantic import BaseModel
from google.adk.agents.callback_context import CallbackContext
from collections.abc import Callable

def validate_state(
    requirements: dict[str, type[BaseModel]],
) -> Callable:

    def callback(callback_context: CallbackContext) -> None:

        for key, schema in requirements.items():

            data = callback_context.state.get(key)

            if data is None:
                raise ValueError(
                    f"Missing required state: {key}"
                )

            # Validate data against Pydantic schema
            schema.model_validate(data)

        return None

    return callback