#!/usr/bin/env pytest -vs
"""Tests for Gophish tool functions."""

# Third-Party Libraries
from mock import patch
import pytest

# cisagov Libraries
from tools.gophish_complete import get_campaign_id
from tools.gophish_export import (
    assessment_exists,
    export_targets,
    find_unique_target_clicks_count,
)


class TestComplete:
    """Test gophish-complete script."""

    @pytest.mark.parametrize(
        "campaigns", [{"1": "RV0000-C1", "2": "RV0000-C2", "3": "RV0000-C3"}]
    )
    def test_get_campaign_id_found(self, campaigns):
        """Verify correct campaign id is returned when a valid campaign name is provided."""
        assert get_campaign_id("RV0000-C2", campaigns) == "2"

    @pytest.mark.parametrize(
        "campaigns", [{"1": "RV0000-C1", "2": "RV0000-C2", "3": "RV0000-C3"}]
    )
    def test_get_campaign_id_not_found(self, campaigns):
        """Verify LookupError is raised when searching for unknown campaign id."""
        with pytest.raises(LookupError):
            get_campaign_id("RV0000-C6", campaigns)


class TestExport:
    """Test gophish-export script."""

    @patch("tools.connect")
    def test_assessment_exists_found(self, mock_api, multiple_campaign_object):
        """Verify True is returned when assessment is in Gophish."""
        mock_api.campaigns.get.return_value = multiple_campaign_object

        assert assessment_exists(mock_api, "RVXXX1") is True

    @patch("tools.connect")
    def test_assessment_exists_not_found(self, mock_api, multiple_campaign_object):
        """Verify False is returned when assessment is not in Gophish."""
        mock_api.campaigns.get.return_value = multiple_campaign_object
        assert assessment_exists(mock_api, "RVXXX3") is False

    @patch("tools.connect")
    def test_find_unique_target_clicks_count(self, mock_api, multiple_click_object):
        """Verify that the correct number of unique users in a click list is found."""
        assert find_unique_target_clicks_count(multiple_click_object) == 4

    def mock_get_group_ids(self, s, group_object):
        """Return a mock list of Gophish group objects."""
        return group_object

    # Mocks the group id's returned for the assessment's groups.
    @patch("tools.gophish_export.get_group_ids", return_value=[1, 2])
    # Mock API to allow Gophish group objects to be returned.
    @patch("tools.connect")
    def test_export_targets(
        self, mock_api, mock_export, multiple_gophish_group_object, email_target_json
    ):
        """Verify the appropriate JSON is created by export targets."""
        mock_api.groups.get.side_effect = multiple_gophish_group_object

        assert export_targets(mock_api, "RVXXX1") == email_target_json
