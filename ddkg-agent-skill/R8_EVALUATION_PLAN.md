# R8 cross-assistant evaluation plan

## Object of evaluation

The object evaluated is the frozen R8 `ddkg.skill` artifact, not the relative performance of individual LLMs.

## Assistant environments

The planned evaluation uses independent model families, including hosted and open-weight environments. For each run, record the exact model name/version or endpoint. For local models also record model tag, digest when available, quantization, runtime version, and relevant hardware.

## Reporting

For each predefined criterion, report only how many independent assistants satisfy it, for example `5/5`, `4/5`, `3/5`, `2/5`, `1/5`, or `0/5`. Do not publish an overall leaderboard or model ranking.

Where one test has several independent criteria, report those findings separately rather than collapsing them into a model score.

## Regression and generalization

Tiers 0 through 7 are regression/behavioral tests because findings from those tiers informed R8. They do not support an orthogonal-generalization claim.

A new Tier 8 is generated only after R8 is frozen. It should contain at least nine questions and record a coverage map at generation time, including:

- source(s) exercised;
- query construction or graph operation exercised;
- silent-failure class or interpretation rule exercised;
- confirmation that the relevant entity/example was not used to tune R8 for that behavior.

Tier 8 question authorship must not privilege an evaluated assistant. Preferred design: derive candidate coverage mechanically from the frozen archive and have the project lead finalize the scientific questions, or use a separate assistant that is not evaluated on Tier 8.

## Delivery of the skill

If a client cannot ingest a `.skill` archive natively, use a model-neutral delivery harness that exposes the same frozen archive contents and routing behavior. Supplying only `SKILL.md` is not a test of the full compositional skill.

## Freeze rule

No Tier 8 prompt or replacement test anchor may be used to tune R8 before the formal evaluation. After the final archive is frozen, R8 is immutable through all assistant runs. New defects are recorded as results rather than repaired during the experiment.
