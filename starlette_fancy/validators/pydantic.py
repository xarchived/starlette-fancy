from typing import Type, Union, Literal

from pydantic import (
    BaseModel as PydanticModel,
    validate_model,
    ValidationError,
    MissingError,  # noqa
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
    request_query_model: Type[PydanticModel]
    request_body_model: Type[PydanticModel]
    response_body_model: Type[PydanticModel]

    async def __call__(
        self,
        data: Union[list, dict],
        source: Literal["body", "query_params"] = "body",
        response: bool = False,
        partial: bool = False,
    ) -> dict:
        if response:
            if hasattr(self, "response_body_model"):
                validate_input_and_raise(
                    model=self.response_body_model,
                    input_data=data,
                    partial=partial,
                )
        else:
            if hasattr(self, "request_body_model") and source == "body":
                validate_input_and_raise(
                    model=self.request_body_model,
                    input_data=data,
                    partial=partial,
                )
            if (
                hasattr(self, "request_query_model")
                and source == "query_params"
            ):
                validate_input_and_raise(
                    model=self.request_query_model,
                    input_data=data,
                    partial=partial,
                )

        return data
