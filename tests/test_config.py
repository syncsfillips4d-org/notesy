import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def import_main(extra_env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    for name in (
        "FLY_APP_NAME",
        "BACKEND_URL",
        "BACKEND_KEY",
        "SESSION_SECRET",
        "OWNER_EMAIL",
        "ANTHROPIC_API_KEY",
    ):
        env.pop(name, None)
    env.update(extra_env)
    return subprocess.run(
        [sys.executable, "-c", "import app.main; print('ok')"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class FlyConfigTests(unittest.TestCase):
    def test_local_import_uses_defaults(self) -> None:
        proc = import_main({})

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("ok", proc.stdout)

    def test_fly_requires_owner_email_and_anthropic_key(self) -> None:
        proc = import_main(
            {
                "FLY_APP_NAME": "notesy-local",
                "BACKEND_URL": "https://example.test/v1",
                "BACKEND_KEY": "dev-key",
                "SESSION_SECRET": "dev-secret",
            }
        )

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("OWNER_EMAIL", proc.stderr)
        self.assertIn("ANTHROPIC_API_KEY", proc.stderr)

    def test_fly_imports_with_required_env(self) -> None:
        proc = import_main(
            {
                "FLY_APP_NAME": "notesy-local",
                "BACKEND_URL": "https://example.test/v1",
                "BACKEND_KEY": "dev-key",
                "SESSION_SECRET": "dev-secret",
                "OWNER_EMAIL": "me@example.com",
                "ANTHROPIC_API_KEY": "test-key",
            }
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("ok", proc.stdout)


if __name__ == "__main__":
    unittest.main()
