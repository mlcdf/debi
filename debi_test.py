
import delegator


class TestDebi:

    def test_package_64bits(self):
        assert delegator.run('debi atom atom').return_code == 0

    def test_package_64bits_beta(self):
        assert delegator.run('debi atom atom --beta').return_code == 0

    def test_package_32bits(self):
        assert delegator.run(
            'debi webtorrent webtorrent-desktop').return_code == 0
