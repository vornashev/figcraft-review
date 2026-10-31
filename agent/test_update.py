"""python3 -m unittest agent/test_update.py — picking a release and checking its installer, with a fake GitHub."""
import hashlib
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update  # noqa: E402


def release(tag, pre=False, draft=False, assets=()):
    return {"tag_name": tag, "prerelease": pre, "draft": draft, "html_url": f"https://example/{tag}", "body": "notes",
            "assets": [{"name": a, "browser_download_url": f"https://example/{tag}/{a}"} for a in assets]}


class Versions(unittest.TestCase):
    def test_semver_order(self):
        order = ["0.4.9", "0.5.0-alpha", "0.5.0-rc.2", "0.5.0-rc.10", "0.5.0", "0.5.1", "0.10.0", "1.0.0"]
        self.assertEqual(sorted(reversed(order), key=update.key), order)
        self.assertIsNone(update.key("latest"))

    def test_newest_release(self):
        rs = [release("v0.5.1"), release("v0.6.0-rc.1", pre=True), release("v0.7.0", draft=True), release("nightly")]
        self.assertEqual(update.newest(rs, "0.5.0")["version"], "0.5.1", "a stable copy isn't offered prereleases or drafts")
        self.assertEqual(update.newest(rs, "0.5.0-rc.1")["version"], "0.6.0-rc.1", "a prerelease follows prereleases")
        self.assertIsNone(update.newest(rs, "0.5.1"))
        self.assertEqual(update.newest([release("v0.5.0")], "0.5.0-rc.2")["version"], "0.5.0", "an rc moves on to its release")

    def test_asset_per_os(self):
        with mock.patch.object(update.desktop, "WINDOWS", True), mock.patch.object(update.desktop, "MAC", False):
            self.assertEqual(update.asset_name("1.0.0"), "FigCraftReview-Setup-v1.0.0.exe")
        with mock.patch.object(update.desktop, "WINDOWS", False), mock.patch.object(update.desktop, "MAC", True), \
                mock.patch.object(update.platform, "machine", return_value="arm64"):
            self.assertEqual(update.asset_name("1.0.0"), "FigCraftReview-v1.0.0-macos-arm64.dmg")
        with mock.patch.object(update.desktop, "WINDOWS", False), mock.patch.object(update.desktop, "MAC", False):
            self.assertIsNone(update.asset_name("1.0.0"))


class Download(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        win = mock.patch.multiple(update.desktop, WINDOWS=True, MAC=False)
        win.start()
        self.addCleanup(win.stop)
        self.name = "FigCraftReview-Setup-v1.0.0.exe"
        self.found = update.newest([release("v1.0.0", assets=[self.name, "SHA256SUMS"])], "0.5.0")

    def fake(self, body, sums):
        files = {f"https://example/v1.0.0/{self.name}": body, "https://example/v1.0.0/SHA256SUMS": sums.encode()}
        return mock.patch.object(update, "_get", side_effect=lambda url, timeout=30: files[url])

    def test_the_installer_is_kept_only_when_its_checksum_matches(self):
        body = b"setup"
        with self.fake(body, f"{hashlib.sha256(body).hexdigest()}  {self.name}\nabc  other.zip\n"):
            path = update.download(self.found, self.tmp.name)
        with open(path, "rb") as f:
            self.assertEqual(f.read(), body)
        with self.fake(b"tampered", f"{hashlib.sha256(body).hexdigest()}  {self.name}\n"), self.assertRaises(ValueError):
            update.download(self.found, self.tmp.name)
        with self.fake(body, "abc  other.zip\n"), self.assertRaises(ValueError):
            update.download(self.found, self.tmp.name)

    def test_check_asks_github_once_a_day(self):
        cache = os.path.join(self.tmp.name, "update.json")
        api = json.dumps([release("v9.0.0", assets=["SHA256SUMS"])]).encode()
        with mock.patch.object(update, "CACHE", cache), mock.patch.object(update, "_get", return_value=api) as get:
            self.assertEqual(update.check()["version"], "9.0.0")
            self.assertEqual(update.check()["version"], "9.0.0")
            self.assertEqual(get.call_count, 1)
            update.check(force=True)
            self.assertEqual(get.call_count, 2)
        with mock.patch.object(update, "CACHE", os.path.join(self.tmp.name, "none.json")), \
                mock.patch.object(update, "_get", side_effect=OSError("offline")):
            self.assertIsNone(update.check(), "offline: no update, no error")

    def test_a_checkout_is_sent_to_the_release_page(self):
        with mock.patch.object(update, "installed", return_value=False):
            self.assertEqual(update.summary(self.found), {"version": "1.0.0", "url": "https://example/v1.0.0", "auto": False})


if __name__ == "__main__":
    unittest.main()
