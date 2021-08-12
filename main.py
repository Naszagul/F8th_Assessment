from fastapi import FastAPI, Request, Body, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel, Field


app = FastAPI(
    title="API",
    version="0.0.01",
    description="This is the API for the QA Engineer Assessment"
)


# allow and restrict all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Collect the API key into the header
X_API_KEY = APIKeyHeader(name='X-API-Key')


# create error response model
class HTTPError(BaseModel):
    detail: str = Field(..., example="Error message")


error_response_models = {
    401: {"model": HTTPError},
    402: {"model": HTTPError},
    403: {"model": HTTPError},
    422: {"model": HTTPError},
    503: {"model": HTTPError},
}


"""
Route to get the status of the service
"""


class ServerResponse(BaseModel):
    server: str = Field("ok", example="ok")


@app.get("/", tags=[""], response_model=ServerResponse)
def server_response():
    # return the success message
    return JSONResponse(content={"server": "ok"})


"""
a client want to create a session ID
"""


class Sessions(BaseModel):
    timestamp: int = Field(
        ...,
        example=1619605207269,
        title="The timestamp of the session started",
        ge=1,
        le=9999999999999
    )
    ip: str = Field(
        ...,
        example="10.20.30.40",
        title="The IP of the user who starts the session",
        max_length=45
    )
    url: str = Field(
        ...,
        example="https://www.example.com/of/your/website?var=included",
        title="The URL of the session started",
        max_length=2048
    )
    group_id: Optional[str] = Field(
        "",
        example="nbm0lsybmheyue42zst3y1vn",
        title="The group ID of the session started",
        max_length=64
    )
    user_id: Optional[str] = Field(
        "",
        example="Bob01",
        title="The user ID of the session started",
        max_length=64
    )
    branch_id: Optional[str] = Field(
        "",
        example="branch-001",
        title="The branch ID of the session started",
        max_length=64
    )


class SessionsResponse(BaseModel):
    id: int = Field(
        ...,
        example=294,
        title="The session ID created",
        ge=1,
        le=9223372036854775807
    )
    request: Sessions


@app.post("/sessions/", tags=["Sessions"], status_code=201, response_model=SessionsResponse, responses=error_response_models)
async def sessions(request: Request, data: Sessions, api_key: str = Depends(X_API_KEY)):

    response = "Fake response for the assessment purposes"

    # return the session id
    return JSONResponse(status_code=201, content=response)


"""
a client want to check the authenticity of an user
"""


class AuthCheckScore(BaseModel):
    risk: Optional[int] = Field(
        None,
        example=43,
        title="The score of the risk total",
        ge=1,
        le=100
    )
    authenticity: Optional[int] = Field(
        None,
        example=77,
        title="The score of the risk of account takeover",
        ge=1,
        le=100
    )
    web_bot: Optional[int] = Field(
        None,
        example=50,
        title="The score of the risk of web bot attack",
        ge=1,
        le=100
    )
    insider_threat: Optional[int] = Field(
        None,
        example=36,
        title="The score of the risk of insider threat",
        ge=1,
        le=100
    )
    blacklist: Optional[int] = Field(
        None,
        example=94,
        title="The score of the risk of a blacklisted profile",
        ge=1,
        le=100
    )


class AuthCheck(BaseModel):
    session_id: int = Field(
        ...,
        example=294,
        title="The session ID of the user to check the authenticity",
        ge=1,
        le=9223372036854775807
    )
    user_id: Optional[str] = Field(
        "",
        example="Bob01",
        title="The user ID of the user to check the authenticity",
        max_length=64
    )
    policy: AuthCheckScore


class AuthCheckResponse(BaseModel):
    is_auth: bool = Field(
        ...,
        example=0,
        title="The result of the user's auth check"
    )
    score: AuthCheckScore
    request: AuthCheck


@app.post("/auth/check/", tags=["Auth"], response_model=AuthCheckResponse, responses=error_response_models)
async def auth_check(request: Request, data: AuthCheck, api_key: str = Depends(X_API_KEY)):

    r = {"status_code": 200}
    response = "Fake response for the assessment purposes"

    # return the result
    return JSONResponse(status_code=r["status_code"], content=response)
