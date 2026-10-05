# JSON Merge Patch Lab

Transform one supplied synthetic JSON target with one merge-patch value, preserving caller inputs and returning detached target/patch/result snapshots. The lab makes deletion, root replacement, whole-array replacement and typed change detection explicit. It uses Python's standard library and changes no resource/configuration file.

From this folder with Python3.13:

```powershell
python -m merge_lab samples/demo.json
python -m merge_lab samples/demo.json --output fresh-report.json
python -m scripts.demo_reports --output another-fresh-report.json
```

The demo intentionally exits1 because the value changed. Exit0 means complete/unchanged;1 means complete/changed;2 means invalid/limit/I/O;3 means fully admitted common shape with unknown schema. Output files must be fresh. No pip/install command is needed. Example envelope:

```json
{"schema":"merge-patch-lab/1","target":{"keep":null,"gone":0},"patch":{"gone":null}}
```

The result retains keep:null and removes gone. A root null patch instead replaces the entire target. Arrays replace whole values; their contents, including object-null fields, stay literal. An object patch applied to a scalar/array/null begins with an empty object. Exact member names remain distinct; no normalization, pointer decoding or path operations occur. These semantics are grounded in [RFC7396](https://www.rfc-editor.org/rfc/rfc7396.html), within this deliberately narrower integer/scalar/resource profile.

## Architecture and API

`merge_lab.contract.parse(bytes)` bounds raw input/lexical work, rejects duplicate decoded keys and admits the entire envelope. `merge_lab.model.analyze(envelope)` independently admits exact builtins and returns a report/status, raising fixed LabError/Unsupported failures. All branches are checked before schema support or transformation, even values that a patch would discard. `render(report)` serializes an already admitted report; it is not an arbitrary-object admission API. The CLI adds bounded regular-file input and checked exclusive output. Demo uses that same CLI.

The private model clones only admitted dict/list/scalar values; no generic deepcopy/user hooks. Native shared acyclic subtrees count at every logical occurrence and yield independently detached snapshots; active cycles fail. Type identity precedes equality/hash/iteration checks. The changed flag compares exact types, recursive values, object names without insertion-order significance, and list elements with order. False differs from integer0. Sorted ASCII JSON makes equivalent object-order reports deterministic; original text/number spelling is not preserved.

## Bounds and security

PLAN.md/fixtures/oracles.json specify all frozen bounds and diagnostics:32KiB input, depth8 including envelope, integer lexeme32, integers within ±9007199254740991, exact builtins, valid non-noncharacter Unicode scalars,512 nodes/64 containers/2048 text-key scalars in each source. Result has conservative1024/128/4096 bounds and standalone depth7. Global native admission is separately bounded before fields are interpreted. Reject fractions/exponents/nonfinite values, negative-zero text, BOM/invalid UTF-8, trailing content, duplicate names and invalid shapes. Native parsed objects cannot reveal prior numeric spelling.

One merge can combine source object trees, not recursively expand copy operations. Tight union maxima are1023 nodes/127 containers; conservative result overflows are not reachable under admitted source bounds. Four-byte-per-scalar UTF-8 caps and some global limits are redundant safety assertions; no impossible boundary test is claimed. Report snapshots still amplify escaped text: the measured32+32 disjoint-key supplementary-scalar fixture is16118 raw UTF-8 bytes but94123 ASCII report bytes. Serialization rejects it before delivery at65536, including newline.

Reports intentionally disclose supplied synthetic values; fixed error JSON omits filenames/documents/OS details. Checked writes require exact integer counts, check flush/close failures and sanitize dirty output/error sinks to preserve exit2 even with actual closed readers. No existing output/input is overwritten. Physical failures can leave partial stdout or a partial newly created file. Hostile filesystem races, atomic delivery, concurrent caller mutation, production authorization/identity policy and private documents are outside the model.

There is no RFC6902 operation engine, JSONPath/eval, diff/minimal patch generation, merge sequence, external lookup, HTTP/service/API call, new repository or publication. An operation-looking list is just a replacement array; op/path object names are just data. No full RFC/general-JSON conformance or real resource-change authorization is claimed.

## Verified checks

```powershell
python -m unittest discover -v
python -O -m unittest discover -v
python -m compileall -q merge_lab scripts tests
python -m scripts.mutation_check fresh-mutation-directory
python -m bandit -r merge_lab scripts/demo_reports.py
```

Observed on Windows CPython3.13.7:32 normal and32 optimized tests/no skips,40 complete original independent reports and6 fixed diagnostic/status cases frozen before core, actual optimized CLI/demo children, no-hook/cycle/alias/snapshot checks, strict admission, real closed pipes, exclusive/hardlink/empty/NUL paths and dirty short/flush/close failures. Six mutants each fail one independent assertion; originals stay unchanged. Secondary idempotence complements the fixed expectations rather than replacing them.

Bandit1.9.4 runtime/demo scope:302 lines, zero remaining findings/errors, one narrow B105 false-positive skip for negative-zero numeric spelling. Tests and trusted mutation/receipt tooling are outside that scan scope. ECC self-review fixed noninteger write-count acceptance; before/after regression evidence is retained. The initial sandbox hardlink denial is preserved; app-approved reruns verified it without skips. Other Python patches/platforms, full conformance, hosted CI and independent audit remain unverified. See VALIDATION.md/REVIEW.md and the private final hash receipt.

## Sources, license and learning

RESEARCH.md records RFC7396/RFC6902 comparison and actual pinned candidate source/tests/license/setup/CI/issues. Fifteen private captures matched inspected blobs and were never executed/adopted. Runtime and delivery tests adapt owned prior Pointer lab patterns; the original hand-specified merge oracles were frozen before code. Candidate captures retain their licenses and are separate from the public original lab's MIT LICENSE/NOTICE.md.

Codex assisted design, implementation, fixtures, checks, review and docs; Jake retains manual publication/merge decisions. A bounded loopback Ollama label draft was reviewed, corrected and preserved; worker output is not security/correctness evidence. No remote inference, installation or new spending. LEARNING.md explains the distinctions and review lesson.

Optional exercise: compare a member-null patch with a root-null patch, then place that null inside a replacement array and predict the result before running it.

## Publication status

See [publication review](PUBLICATION.md) for the October 5 source snapshot, fresh local checks, evidence boundaries and current hosted-check distinction.
