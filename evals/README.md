# Behavioral evaluation cases

These cases test decisions and boundaries, not exact wording. Run them with an independent agent when materially revising a skill. Give the evaluator only the named skill, the request, and any minimal synthetic artifacts; do not reveal the expected result until after the output is produced.

Evaluate every `must_do` and `must_not_do` item in `cases.json`. Save generated outputs outside the repository unless they are fully synthetic and intentionally added as maintained fixtures.

The repository validator confirms this file is valid JSON, but it cannot prove model behavior. A release should record which cases were forward-tested and what narrow changes were made in response.
