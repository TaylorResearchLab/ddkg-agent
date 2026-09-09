# R8 candidate status

The R8 release candidate has been built deterministically from the hardened source tree and has passed routing validation plus generic public-hygiene checks.

Current candidate identity is recorded in `R8_BUILD.md`.

R8 is **not yet formally frozen for evaluation**. The remaining requirements are the deployment-specific denylist checks on source and archive and the focused live engineering regressions listed in `R8_REVIEW_CHECKLIST.md` and `R8_ENGINEERING_REGRESSION.md`.

No formal Tier 8 orthogonal questions should be generated or used to tune the skill until those pre-freeze checks are complete and the archive is declared immutable.
