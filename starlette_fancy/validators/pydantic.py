from typing import Type, Union, Literal

# noinspection PyProtectedMember
from pydantic import (
    BaseModel as PydanticModel,
    validate_model,
    ValidationError,
    MissingError,
)

from starlette_fancy.validators import Validator


def validate_input_and_raise(
    model: Type[PydanticModel],
    input_data: dict,
    partial: bool = False,
) -> None:
    e: ValidationError
    _, _, e = validate_model(model=model, input_data=input_data)
    if e:
        if not partial:
            raise e

        errors: list = []
        for error in e.raw_errors:
            if isinstance(error.exc, MissingError):
                continue
            errors.append(error)
        if errors:
            raise ValidationError(errors=errors, model=model)


class PydanticValidator(Validator):
    params_model: Type[PydanticModel]
    request_model: Type[PydanticModel]
    response_model: Type[PydanticModel]

    async def __call__(
        self,
        data: Union[list, dict],
        source: Literal["body", "query_params"] = "body",
        response: bool = False,
        partial: bool = False,
    ) -> dict:
        if response:
            if hasattr(self, "response_model"):
                validate_input_and_raise(
                    model=self.response_model,
                    input_data=data,
                    partial=partial,
                )
        else:
            if hasattr(self, "request_model") and source == "body":
                validate_input_and_raise(
                    model=self.request_model,
                    input_data=data,
                    partial=partial,
                )
            if hasattr(self, "params_model") and source == "query_params":
                validate_input_and_raise(
                    model=self.params_model,
                    input_data=data,
                    partial=partial,
                )

        return data
