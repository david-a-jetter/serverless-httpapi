from unittest.mock import patch, MagicMock

from faker import Faker

from hearty.oura.manager import OuraUserAuthManager, OuraDataManager
from hearty.oura.models import OuraUserAuth, PersonalInfo
from tests.test_oura.factories import (
    OuraAuthCodeRequestFactory,
    OuraUserAuthFactory,
    PersonalInfoFactory,
)

fake = Faker()


@patch("hearty.oura.manager.OuraUserAuthorizer.build")
@patch("hearty.oura.manager.DynamoHashKeyedRepository.build")
def test_auth_manager_build(db_build, auth_build):
    db = MagicMock()
    db_build.return_value = db
    auth = MagicMock()
    auth_build.return_value = auth
    environment = fake.bs()
    manager = OuraUserAuthManager.build(environment)

    assert auth_build.call_args[0][0] == environment

    args, kwargs = db_build.call_args
    assert kwargs["item_class"] == OuraUserAuth
    assert kwargs["key_attribute"] == "user_id"
    assert kwargs["environment"] == environment
    assert kwargs["table_name"] == "OuraUserAuth"

    assert manager._authorizer == auth
    assert manager._storage == db


def test_auth_manager_authorize_first_time():
    auth = MagicMock()
    db = MagicMock()
    manager = OuraUserAuthManager(auth, db)
    user_id = fake.bs()
    request = OuraAuthCodeRequestFactory()
    auth_response = OuraUserAuthFactory()
    auth.authorize_user.return_value = auth_response

    manager.authorize_first_time(user_id, request)

    assert auth.authorize_user.call_args[0][0] == request

    args, kwargs = db.save_item.call_args
    assert args[0] == user_id
    assert args[1] == auth_response


def test_auth_manager_refresh_auth():
    existing_auth = OuraUserAuthFactory()
    user_id = fake.bs()
    new_auth = OuraUserAuthFactory()
    auth = MagicMock()
    auth.refresh_user.return_value = new_auth
    db = MagicMock()
    db.get_item.return_value = existing_auth
    manager = OuraUserAuthManager(auth, db)

    manager.refresh_authorization(user_id)

    assert db.get_item.call_args[0][0] == user_id
    assert auth.refresh_user.call_args[0][0] == existing_auth.refresh_token

    args, kwargs = db.save_item.call_args
    assert args[0] == user_id
    assert args[1] == new_auth


def test_auth_manager_refresh_auth_existing_none():
    user_id = fake.bs()
    db = MagicMock()
    db.get_item.return_value = None
    manager = OuraUserAuthManager(MagicMock(), db)

    try:
        manager.refresh_authorization(user_id)
    except Exception as ex:
        assert isinstance(ex, ValueError)
        assert user_id in str(ex)


def test_auth_manager_get_user_auth():
    existing_auth = OuraUserAuthFactory()
    db = MagicMock()
    db.get_item.return_value = existing_auth
    user_id = fake.bs()
    manager = OuraUserAuthManager(MagicMock(), db)

    actual_auth = manager.get_user_auth(user_id)

    assert actual_auth == existing_auth
    assert db.get_item.call_args[0][0] == user_id


@patch("hearty.oura.manager.OuraUserAuthManager.build")
@patch("hearty.oura.manager.DynamoHashKeyedRepository.build")
@patch("hearty.oura.manager.OuraApiAccess.build")
def test_data_manager_build(api_build, db_build, auth_build):
    pi_db = MagicMock()
    db_build.return_value = pi_db
    auth = MagicMock()
    auth_build.return_value = auth
    environment = fake.bs()
    user_id = fake.bs()
    existing_auth = OuraUserAuthFactory()
    auth.get_user_auth.return_value = existing_auth
    api = MagicMock()
    api_build.return_value = api

    manager = OuraDataManager.build(environment, user_id)

    assert auth_build.call_args[0][0] == environment
    assert api_build.call_args[0][0] == existing_auth.access_token

    pi_args, pi_kwargs = db_build.call_args_list[0]
    assert pi_kwargs["item_class"] == PersonalInfo
    assert pi_kwargs["key_attribute"] == "user_id"
    assert pi_kwargs["environment"] == environment
    assert pi_kwargs["table_name"] == "OuraUserInfo"

    assert manager._user_id == user_id
    assert manager._api == api
    assert manager._user_info == pi_db


@patch("hearty.oura.manager.OuraUserAuthManager.build")
def test_data_manager_build_existing_auth_none(auth_build):

    auth = MagicMock()
    auth.get_user_auth.return_value = None
    auth_build.return_value = auth
    user_id = fake.bs()

    try:
        OuraDataManager.build(fake.bs(), user_id)
    except Exception as ex:
        assert isinstance(ex, ValueError)
        assert user_id in str(ex)


def test_data_manager_fetch_personal_data():
    api = MagicMock()
    personal_info = PersonalInfoFactory()
    api.get_personal_info.return_value = personal_info
    pi_db = MagicMock()
    user_id = fake.bs()
    manager = OuraDataManager(user_id, api, pi_db)

    manager.fetch_personal_info()

    args, kwargs = pi_db.save_item.call_args
    assert args[0] == user_id
    assert args[1] == personal_info
