from unittest.mock import patch, MagicMock

import pytest
from faker import Faker
from requests import HTTPError

from hearty.oura.api import OuraUserAuthorizer, OuraApiAccess
from tests.factories import CredentialFactory
from tests.test_oura.factories import (
    OuraUserAuthFactory,
    AuthCodeRequestFactory,
    PersonalInfoFactory,
)

fake = Faker()


@patch("hearty.oura.api.build_credentials_repo")
def test_auth_build(build_cred_repo):
    cred_repo = MagicMock()
    build_cred_repo.return_value = cred_repo
    credential = CredentialFactory()
    cred_repo.get_item.return_value = credential

    env = fake.bothify()
    authorizer = OuraUserAuthorizer.build(env)

    assert authorizer._session.auth == (credential.client_id, credential.client_secret)
    assert build_cred_repo.call_args[0][0] == env
    assert cred_repo.get_item.call_args[0][0] == "oura"


@patch("hearty.oura.api.build_credentials_repo")
def test_auth_build_null_client_id(build_cred_repo):
    cred_repo = MagicMock()
    build_cred_repo.return_value = cred_repo
    credential = CredentialFactory(client_id=None)
    cred_repo.get_item.return_value = credential

    env = fake.bothify()
    with pytest.raises(ValueError):
        OuraUserAuthorizer.build(env)


@patch("hearty.oura.api.build_credentials_repo")
def test_auth_build_null_client_secret(build_cred_repo):
    cred_repo = MagicMock()
    build_cred_repo.return_value = cred_repo
    credential = CredentialFactory(client_secret=None)
    cred_repo.get_item.return_value = credential

    env = fake.bothify()
    with pytest.raises(ValueError):
        OuraUserAuthorizer.build(env)


def test_authorize_user():

    session = MagicMock()
    authorizer = OuraUserAuthorizer(session)
    response = MagicMock()
    response_obj = OuraUserAuthFactory()
    response.text = response_obj.json()
    session.post.return_value = response
    auth_request = AuthCodeRequestFactory()

    user_auth = authorizer.authorize_user(auth_request)
    assert user_auth == response_obj

    args, kwargs = session.post.call_args

    assert args[0] == "https://api.ouraring.com/oauth/token"
    form = kwargs["data"]
    assert form["grant_type"] == "authorization_code"
    assert form["code"] == auth_request.code
    assert form["redirect_uri"] == auth_request.redirect_uri


def test_authorize_user_null_redirect():

    session = MagicMock()
    authorizer = OuraUserAuthorizer(session)
    response = MagicMock()
    response_obj = OuraUserAuthFactory()
    response.text = response_obj.json()
    session.post.return_value = response
    auth_request = AuthCodeRequestFactory(redirect_uri=None)

    user_auth = authorizer.authorize_user(auth_request)
    assert user_auth == response_obj

    args, kwargs = session.post.call_args

    assert args[0] == "https://api.ouraring.com/oauth/token"
    form = kwargs["data"]
    assert form["grant_type"] == "authorization_code"
    assert form["code"] == auth_request.code
    assert "redirect_uri" not in form


def test_authorize_user_error():

    session = MagicMock()
    authorizer = OuraUserAuthorizer(session)
    response = MagicMock()
    response.ok = False
    session.post.return_value = response
    auth_request = AuthCodeRequestFactory()

    with pytest.raises(HTTPError):
        authorizer.authorize_user(auth_request)


def test_refresh_user():

    session = MagicMock()
    authorizer = OuraUserAuthorizer(session)
    response = MagicMock()
    response_obj = OuraUserAuthFactory()
    response.text = response_obj.json()
    session.post.return_value = response
    refresh_token = fake.bothify()

    user_auth = authorizer.refresh_user(refresh_token)
    assert user_auth == response_obj

    args, kwargs = session.post.call_args

    assert args[0] == "https://api.ouraring.com/oauth/token"
    form = kwargs["data"]
    assert form["grant_type"] == "refresh_token"
    assert form["refresh_token"] == refresh_token


def test_api_build():
    access_token = fake.bothify()
    api = OuraApiAccess.build(access_token)

    assert api._session.headers["Authorization"] == f"Bearer {access_token}"


def test_get_personal_info():
    session = MagicMock()
    api = OuraApiAccess(session)
    response_obj = PersonalInfoFactory()
    response = MagicMock()
    response.text = response_obj.json()
    session.get.return_value = response

    info = api.get_personal_info()
    assert info == response_obj
    assert session.get.call_args[0][0] == "https://api.ouraring.com/v1/userinfo"


def test_get_personal_info_error():
    session = MagicMock()
    api = OuraApiAccess(session)
    response = MagicMock()
    response.ok = False
    session.get.return_value = response

    with pytest.raises(HTTPError):
        api.get_personal_info()
