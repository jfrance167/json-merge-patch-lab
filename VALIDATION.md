# Local verification

Environment: Windows, installed CPython3.13.7, Bandit1.9.4. No new dependency/model installation or remote inference. Initial target only; other patches/platforms, full conformance, hosted CI and independent audit are unverified.

| Check | Outcome | Evidence under .private/verification |
|---|---|---|
| python -m unittest discover -v |PASS exit0,32 tests/no skips|final-normal.log|
| python -O -m unittest discover -v |PASS exit0,32 tests/no skips|final-optimized.log|
| Six assertion mutants |PASS harness0; each mutant1/one assertion failure; originals unchanged|mutations-final/summary.json and raw result.log files|
| Compile runtime/scripts/tests |PASS exit0|compile.log|
| Bandit runtime/demo |PASS exit0,302 LOC,0 findings/errors,1 B105 false-positive skip|bandit-final.json/log|
|40 complete independent original reports/6 fixed diagnostics |Frozen before core; original SHA256 unchanged|research/freeze-v1.json, fixtures/oracles.json, tests|
| Actual CLI/demo and output amplification |PASS normal/-O children and checked delivery|suite logs, amplification.json, samples/demo-report.json|
| Current source/evidence receipt |Generated and independently rehashed before handoff|final-receipt.json, receipt-rehash.json|

Frozen oracle SHA256:4a9afc1eb0e5a9ac9eeb1fa570e9e84290017089a898c6b7032495e082587c77. The pre-core freeze binds PLAN, authoring helper and full fixture bytes; it is a historical contract freeze, not a mutable-doc current manifest. No RFC/upstream vector/algorithm was copied into original fixtures/core. Fifteen private candidate captures match inspected blobs and retain licenses; they were not executed/adopted.

Full report tests cover the fixed null/root/object/array/name/false-zero/order distinctions, including literal object-null fields within a replacement array. Secondary idempotence uses expected original results but is not an independent oracle set. Native tests cover detached input/report siblings, cross-source aliases, cycles and benign subclass/metaclass/hash/iteration/copy-hook rejection. Full discarded/replaced branches are validated before unsupported/merge; lexical depth/number gates assert the decoder was not called. Resource tests exercise feasible raw/node/container/depth/text/integer/output boundaries. No inaccessible result-union overflow test or exponential growth claim.

The disjoint32+32 keys/60 supplementary scalars case is admitted:16118 input UTF-8 bytes,64 result members,94123 ASCII report bytes including newline, rejected before stdout/file creation at65536. Cap-weakening to131072 is an independent assertion mutant alongside null retention, array concatenation, scalar preservation, name normalization and patch aliasing. All six targeted tests fail assertions, not import/syntax errors, and current source hashes match originals after runs.

CLI checks include40 full actual reports/five raw errors plus separate output-limit case, optimized children, help/misuse, empty/fresh/existing/NUL/input-alias/hardlink paths, pre/post metadata observations, dirty write/short/flush/close failures and real closed stdout/stderr readers with a barrier. Physical output-close failure is simulated; pipes are actual. Fixed errors omit document/path/OS details. Partial physical output remains possible; no hostile race or atomicity test.

Preserved initial sandbox run:30 tests,29 passed/one hardlink PermissionError; app-approved31/then32-test reruns verified hardlinks with no skips. ECC writer regression failed on float3.0, then passed after exact-int validation; normal/-O/full mutations were refreshed. Intermediate31-test and mutation-v1 logs remain chronological evidence, not final acceptance. Final Bandit rule-specific annotation yields skipped_tests1/nosec0; scope excludes tests/mutation/receipt tooling. Targeted source credential signatures are not a full secret/history scanner. No own repository/history or hosted baseline exists under approved scope.
