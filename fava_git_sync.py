"""Git sync for Fava
"""

from __future__ import annotations

import datetime
from pathlib import Path
from subprocess import call
from subprocess import DEVNULL

from fava.ext import FavaExtensionBase, extension_endpoint
from flask.wrappers import Response

class FavaGitSync(FavaExtensionBase):
    """Git sync for Fava"""

    has_js_module = True

    @extension_endpoint("sync", ["GET"])
    def sync(self) -> Response:
        st = self._run(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"])
        if st != 1:
            return Response("", 200)

        print(Path(self.ledger.beancount_file_path).name)
        st = self._run(["git", "add", Path(self.ledger.beancount_file_path).name])
        if st != 0:
            return Response("", 500)

        now = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        st = self._run(["git", "commit", "-m", now])
        if st != 0:
            return Response("", 500)

        st = self._run(["git", "push", "--quiet"])
        if st != 0:
            return Response("", 500)

        return Response("", 200)


    @extension_endpoint("status", ["GET"])
    def status(self) -> Response:
        """250 -> git dirty, 200 -> clean"""
        st = self._run(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"])
        if st == 1:
            return Response("", 250)
        return Response("", 200)

    def _run(self, args: list[str]) -> int:
        cwd = Path(self.ledger.beancount_file_path).parent
        return call(args, cwd=cwd, stdout=DEVNULL)