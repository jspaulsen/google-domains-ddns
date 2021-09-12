import os

import pytest

import google_domain_ddns


class TestGoogleDomainDdns:
    def test_missing_envar(self, mocker):
        mocker.patch.object(
            google_domain_ddns,
            'missing_req_envar',
            return_value=['SOMETHING_MISSING'],
        )

        with pytest.raises(Exception):
            google_domain_ddns.main()

    def test_invalid_interval(self, mocker):
        os.environ['INTERVAL'] = 'invalid'

        with pytest.raises(ValueError):
            google_domain_ddns.main()

        os.environ['INTERVAL'] = 'PT1M'

        with pytest.raises(ValueError):
            google_domain_ddns.main()

        del os.environ['INTERVAL']


    def test_google_ddns(self, mocker):
        expected_domain = os.getenv('DOMAIN')
        mock_update_ddns = mocker.patch.object(
            google_domain_ddns.DomainClient,
            'update_ddns',
            return_value='badauth',
        )

        google_domain_ddns.main()

        assert mock_update_ddns.called_with((expected_domain))
