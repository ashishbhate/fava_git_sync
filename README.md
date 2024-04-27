# FavaGitSync
A fava extension to sync a ledger file to a git repo on-demand.

## Installation
See https://github.com/beancount/fava/blob/main/src/fava/help/extensions.md or
https://fava.pythonanywhere.com/example-beancount-file/help/extensions
for information on how to install extensions
- Copy the files to where fava can find them
- Add `2010-01-01 custom "fava-extension" "fava_git_sync"` to your ledger file

## About
The extension adds a button to the header at the top of the page. Clicking this button commits and pushes your ledger file to the configured git repo.
Under the hood, the extension just does a `git commit` and `git push`. The extension assumes that you already have a git repo configured for committing and pushing your ledger file changes, with the credentials, current branch, and push strategy (`push.default`) configured correctly, if required.
The commit message is the current date and time in the ISO 8601 format.
The code is quite simple and it should be easy to modify to change its behaviour. I recommend reading through the code in anycase to understand what the button statuses mean.
The code is very lax about error checking, so caveat emptor.
