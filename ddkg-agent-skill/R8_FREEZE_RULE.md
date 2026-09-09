# R8 freeze rule

Before freeze, engineering regressions may use known historical failures to verify that repairs were implemented correctly. These checks are intentionally not orthogonal.

At freeze, the archive identity is recorded and no orthogonal evaluation prompt or replacement test anchor has been used to tune the artifact.

After freeze, the R8 archive is immutable through the complete cross-assistant evaluation. Any newly discovered defect is recorded as a result and may inform a later release, but does not change R8 during evaluation.
