# FavaGitSync
A fava extension to sync a ledger file to a git repo on-demand.

## Installation
See https://github.com/beancount/fava/blob/main/src/fava/help/extensions.md or
https://fava.pythonanywhere.com/example-beancount-file/help/extensions
for information on how to install extensions
- Copy the files to where fava can find them
- Add `2010-01-01 custom "fava-extension" "fava_git_sync"` to your ledger file
- The extension assumes that you already have a git repo configured for
  committing and pushing your ledger file changes, with the correct credentials,
  current branch, and push strategy (`push.default`) configured correctly,
  if required.


## About
The extension adds a "Sync" button to the header at the top of the page.

The number in square brackets, if present, shows the number of commits the remote
is ahead of your local version. No number means your local version is up-to-date
with the remote

The orange circle, if present, indicates that your local version has uncommited
changes.

A "?" or a red back ground indicates an error. See below for the most likely
cause for a sync error. If the issue is not caused by a conflict, make sure you
have set-up git and your repo correctly. See the installation instructions for
more details.

## Behaviour

- If there are no local changes, then clicking the sync button pulls changes
from remote.

- If there are local changes, and your local was up-to-date with remote, then
clicking the sync button commits your changes and pushes to the remote.

- If there are local changes, and unsync'd remote changes, then clicking the
sync button does the following
	- Commits your changes
	- Does a `git pull --rebase` (this tries to replay your changes on top of
	  the newly pulled changes)
	- Push your new changes to the remote.

  THIS IS MOST LIKELY LEAD TO A GIT CONFLICT!

  Most edits to a beancount file are additions of new entries/directives.
  New entries/directives are added to the bottom of the beancount file.
  Attempting to merge/rebase multiple changes to the same location (in this
  case, the bottom of the file), will inevitably lead to a git conflict.

  When this happens:
  1. Resolve the conflict in the fava editor
  2. Click "Save" to save your resolved changes
  4. Click the sync button to push your resolved changes to remote
  5. Repeat until the sync button no longer shows an error.