# R7 build record

- DDKG target: `DataDistillery_2025_04_DEC`
- Bundled files: 38
- Routing relationships: 239
- Archive size: 303258 bytes
- SHA-256: `eca6c7f7461bab113160fe8a4c71260c35fc4350a0b632294d56ef770cbfdb60`

## R7 changes

- Removed the private-deployment index assumption from the shipped schema reference.
- Made index and query-cost guidance deployment-neutral and based on `SHOW INDEXES`.
- Documented the index consequence of function-wrapped `Term.name` predicates.
- Reworked entity-resolution and hand-over recipes to reduce candidates before tolerant name matching.
- Added deterministic source-to-archive rebuilding.

The DDKG schema target is unchanged. R7 is a skill repair for the December 2025 release.
