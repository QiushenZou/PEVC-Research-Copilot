# Release checklist

Use this checklist before creating a public GitHub repository or release.

## Content and rights

- [ ] Confirm every committed file is intended for public distribution.
- [ ] Confirm no data-room document, internal memo, model, transcript, customer list, or personal data is present.
- [ ] Confirm copied or adapted third-party material has a compatible license and clear attribution; otherwise replace it with an original summary and link.
- [ ] Confirm examples do not disclose real confidential deal facts.

## Secrets and privacy

- [ ] Search both the working tree and staged diff for tokens, passwords, cookies, private keys, private URLs, email addresses, and absolute local paths.
- [ ] Inspect generated HTML and JSON outputs, not only source files.
- [ ] Verify ignored private folders were never committed in earlier history.
- [ ] If any credential was ever committed, rotate it before removing it from Git history.

## Package quality

- [ ] Run the Codex skill validator on all three skill folders.
- [ ] Compile and smoke-test the industry-map Python scripts with Python 3.9+.
- [ ] Render a non-confidential sample map and test node clicks, zoom, pan, search, links, and narrow-screen behavior.
- [ ] Check that the README installation commands match the final repository layout.
- [ ] Inspect the final staged diff, then tag the release consistently with `CHANGELOG.md`.
