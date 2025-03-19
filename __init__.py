"""Git sync for Fava"""

from __future__ import annotations

import os
import datetime
from pathlib import Path
import subprocess

from fava.ext import FavaExtensionBase, extension_endpoint
from flask.wrappers import Response


class FavaGitSync(FavaExtensionBase):
    """Git sync for Fava"""

    has_js_module = True

    last_remote_check = None

    remote_check_delay_seconds = 10

    @extension_endpoint("sync", ["GET"])
    def sync(self) -> Response:
        # If we ran into a rebase issue, we only commit and push
        git_dir = self._check_output(["git", "rev-parse", "--git-dir"])
        if git_dir == "error":
            return Response("", 500)
        ledger_folder = Path(self.ledger.beancount_file_path).parent
        if os.path.exists(
            Path.joinpath(ledger_folder, git_dir, "rebase-apply")
        ) or os.path.exists(Path.joinpath(ledger_folder, git_dir, "rebase-merge")):
            return self._rebase_fix()

        have_local_changes = True
        st = self._run(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"])
        if st != 1:
            have_local_changes = False

        if have_local_changes:
            st = self._run(["git", "add", Path(self.ledger.beancount_file_path).name])
            if st != 0:
                return Response("", 500)

            now = (
                datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
            )
            st = self._run(["git", "commit", "-m", now])
            if st != 0:
                return Response("", 500)

        ahead_count = self._get_remote_ahead_count()
        if ahead_count < 0:
            return Response("", 500)
        if ahead_count > 0:
            st = self._run(["git", "pull", "--rebase"])
            if st != 0:
                return Response("", 500)

        if have_local_changes:
            st = self._run(["git", "push", "--quiet"])
            if st != 0:
                return Response("", 500)

        return Response("", 200)

    @extension_endpoint("status", ["GET"])
    def status(self) -> Response:
        """250 -> git dirty, 200 -> clean"""
        remote_ahead_count = ""
        now = datetime.datetime.now()
        if self.last_remote_check == None or (
            (now - self.last_remote_check).total_seconds()
            > self.remote_check_delay_seconds
        ):
            remote_ahead_count = self._get_remote_ahead_count()
            if remote_ahead_count >= 0:
                self.last_remote_check = now

        if remote_ahead_count != "" and remote_ahead_count < 0:
            return Response("", 500)

        st = self._run(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"])
        if st == 1:
            return Response(f"{remote_ahead_count}", 250)

        return Response(f"{remote_ahead_count}", 200)

    def _get_remote_ahead_count(self) -> int:
        st = self._run(["git", "fetch"])
        if st != 0:
            return -1

        current_branch = self._check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        )
        if current_branch == "error":
            return -1

        remote_branch = self._check_output(
            ["git", "rev-parse", "--abbrev-ref", f"{current_branch}@{{upstream}}"]
        )
        if remote_branch == "error":
            return -1

        count_ahead = self._check_output(
            ["git", "rev-list", f"HEAD..{remote_branch}", "--count"]
        )
        if count_ahead == "error":
            return -1

        print("Test", int(count_ahead))
        return int(count_ahead)

    def _rebase_fix(self):
        st = self._run(["git", "add", Path(self.ledger.beancount_file_path).name])
        if st != 0:
            return Response("", 500)

        now = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

        st = self._run(["git", "commit", "-m", f"fixed rebase conflict {now}"])
        if st != 0:
            return Response("", 500)

        st = self._run(["git", "rebase", "--continue"])
        if st != 0:
            return Response("", 500)

        st = self._run(["git", "push", "--quiet"])
        if st != 0:
            return Response("", 500)

        return Response("", 200)

    def _run(self, args: list[str]) -> int:
        cwd = Path(self.ledger.beancount_file_path).parent
        return subprocess.call(args, cwd=cwd, stdout=subprocess.DEVNULL)

    def _check_output(self, args: list[str]) -> str:
        try:
            cwd = Path(self.ledger.beancount_file_path).parent
            return subprocess.check_output(args, text=True, cwd=cwd).strip()
        except:
            return "error"
