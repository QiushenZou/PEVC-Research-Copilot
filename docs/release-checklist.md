# Release checklist

## Content and rights

- [ ] Every committed file is intended for distribution.
- [ ] No data-room document, internal memo, model, transcript, customer/LP list, personal data, or real deal work product is present.
- [ ] Third-party material has compatible rights and attribution; otherwise replace it with an original summary and link.
- [ ] Examples are synthetic or public and cannot be mistaken for a live investment recommendation.

## Secrets and privacy

- [ ] Search working tree, staged diff, generated HTML, JSON, and Git history for tokens, passwords, cookies, private keys, private URLs, emails, and local absolute paths.
- [ ] If a credential was ever committed, rotate it before rewriting history.
- [ ] Confirm optional N.E.I. integration contains no Token or confidential project context.

## Skill quality

- [ ] Run the Codex `quick_validate.py` against all six skill folders.
- [ ] Confirm descriptions route cleanly among fact card, screening, industry map, diligence, and IC work.
- [ ] Confirm the router remains thin and the specialist skills remain independently usable.
- [ ] Confirm references are linked from the relevant `SKILL.md` and no unfinished placeholders remain.

## Deterministic checks

- [ ] Run `python3 scripts/validate_repo.py`.
- [ ] Run `python3 scripts/validate_project_bundle.py examples/synthetic-project --require-decision`.
- [ ] Confirm negative tests fail for project mismatch, valuation mismatch, and return-math mismatch.
- [ ] Compile and smoke-test every Python script with a supported Python version.

## Industry map QA

- [ ] Validate a non-confidential industry JSON file.
- [ ] Render the HTML and inspect initial fit, overlap, arrows, highlight paths, node click behavior, search, links, mouse/trackpad navigation, and narrow-screen behavior.
- [ ] Confirm every node has company-role evidence and its own node explainer.

## Documentation and release

- [ ] Installation commands match the final skill list.
- [ ] The Chinese usage guide covers single-skill and end-to-end workflows.
- [ ] Version and changelog agree.
- [ ] Inspect the final diff, commit, push, and verify CI before tagging the release.
