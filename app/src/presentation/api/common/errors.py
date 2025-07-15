from typing import List, Dict, Union
from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    detail: str

class OpenApiErrorResponseConfig(BaseModel):
    code: int
    description: str
    detail: str

def generate_responses(errors: List[OpenApiErrorResponseConfig]) -> Dict[int, Dict]:
    responses = {}

    for error in errors:
        responses[error.code] = {
            "description": error.description,
            "model": ErrorResponseModel,
            "content": {
                "application/json": {
                    "example": {"detail": error.detail}
                }
            }
        }

    return responses