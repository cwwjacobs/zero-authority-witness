# UKSL: descriptor binding repair

## Map

Scope: PR #1 descriptor TOCTOU evidence binding only. Descriptor actions must
match a separately supplied original witness receipt (source and snapshot digest),
then match the current local materialized descriptor. Missing evidence fails
closed. Validate binding version and complete SHA-256 syntax. Record descriptor
artifacts in the receipt; preserve the no-authority claim.

The CLI selects the receipt from the explicitly selected evidence run, never from
the mutable binding. API callers supply their retained receipt separately. This
is an integrity check against retained witness evidence, not signed provenance:
replacement of the receipt and all evidence is outside this guarantee.

## Execute

Update binding verification, gate plumbing, witness artifact hashes, CLI loading,
schema and scope documentation. Add adversarial descriptor-plus-binding rewrite,
positive verification, and malformed/missing witness evidence regressions.

## Audit gate

Run descriptor regression tests and the full unittest suite; inspect diff for
unrelated behavior changes. Root reviewer must audit before pushing the PR head.

## Audit result

`python -m unittest discover -s tests -q`: 37 tests passed, including 20
descriptor tests. The new API and CLI adversarial cases mutate both descriptor
and binding and are blocked by the retained original witness receipt. Missing
receipt, missing or inconsistent snapshot artifact hashes, invalid versions and
malformed digests fail closed. Unchanged witnessed descriptors still verify.

A pre-existing claim mismatch was narrowed: hashing uses replacement-decoded
UTF-8 text, so docs now state captured text identity rather than arbitrary binary
byte identity. No digest or snapshot format migration was introduced.

The repository's default `unittest discover` finds no tests; explicit `-s tests`
is the repository verification script's documented invocation and was used.
Push remains reserved for the root review; no remote mutation by this worker.
