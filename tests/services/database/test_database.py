from unittest import mock

import pytest

from services.database.database import Database


class TestDatabase:
    @pytest.fixture
    def mock_open(self):
        with mock.patch(
            "services.database.database.open"
        ) as mock_open:
            yield mock_open

    @pytest.fixture
    def mock_database(self):
        with mock.patch(
            "services.database.database.Database.get_database"
        ) as mock_db:
            yield mock_db

    def test_should_save_on_database(self, mock_open, mock_database):
        mock_database.return_value = {}
        Database().save(key="fake_key", data={"foo": "bar"})
        mock_open.assert_called_once()

    @pytest.mark.parametrize("database, expected_response", [
        ({"fake": {"foo": "bar"}}, {"foo": "bar"}),
        ({}, None)
    ])
    def test_should_get_on_database(self, mock_database, database, expected_response):
        mock_database.return_value = database
        response = Database().get("fake")
        assert response == expected_response

