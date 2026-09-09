# R8 release-candidate review checklist

This file records what remains before the R8 artifact is frozen for the cross-assistant evaluation.

## Completed on the R8 branch

- [x] R7 baseline archive SHA-256 verified before R8 edits.
- [x] Reviewed R8 hardening changes applied to curated skill material and routing.
- [x] `route.py --check` passed with 258 routing relationships.
- [x] Deterministic build completed.
- [x] Generic public-hygiene check passed on the source tree.
- [x] Generic public-hygiene check passed on the built archive.
- [x] R8 release-candidate identity recorded in `R8_BUILD.md`.
- [x] Follow-up consistency review removed conflicting display-label guidance.

## Required before freeze

- [ ] Run `check_public_skill_hygiene.py` on the source tree with `--require-denylist` and an external deployment-specific denylist that is not committed to this repository.
- [ ] Run the same required-denylist check on `ddkg.skill`.
- [ ] Run focused engineering regressions for the repaired behaviors against `DataDistillery_2025_04_DEC`. These are repair checks, not the formal cross-assistant evaluation.
- [ ] Confirm the candidate Tier 6.5 replacement does not appear in R8 as an example of the tested behavior; replace it before protocol freeze if contaminated.
- [ ] Generate the new orthogonal Tier 8 from the frozen archive, with at least nine questions and a coverage map of sources, query constructions, and failure classes.
- [ ] Freeze the complete prompt packet with the final R8 SHA-256 and exact model/runtime metadata fields.

## Freeze rule

At freeze time, no new orthogonal evaluation prompt or replacement test anchor may have been used to tune R8. After freeze, the R8 archive is immutable through the formal evaluation. Any defect discovered during that evaluation is recorded as a result rather than repaired in place.
