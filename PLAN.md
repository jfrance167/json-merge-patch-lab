# Proposed JSON Merge Patch lab plan

Status: coordinator approved stages1–5 at04:49 under Jake's direct overnight delegation. Tier3 bounded synthetic portfolio lab. PLAN.md is the requested plan location; tasks/todo.md holds ordered work. No new repository or dependency installation is authorized.

## Problem and success criteria

Demonstrate transformation of a supplied synthetic target by one supplied merge-patch value, while making missing/null/object/array and immutable-input behavior visible. Success means exact bounded admission, a detached result and provenance snapshots, independent complete expected reports/statuses frozen before code, checked local delivery, meaningful mutants and honest verification/learning records. It does not authorize changing an existing file/configuration/resource or establish permission to patch anything.

Recommendation: original stdlib Python RFC7396 teaching profile `merge-patch-lab/1`. RESEARCH.md compares actual candidate code/tests/licenses/CI and RFC6902. Defer operation-list patching, diff/minimal patch generation and networking. Reuse reviewed owned pointer admission/I/O/evidence ideas after approval, without importing or editing the previous lab at runtime.

## Profile and exact value semantics

Input is one UTF-8 JSON envelope with exactly schema, target and patch. schema is 1–64 ASCII letters/digits/slash/period/underscore/hyphen. target and patch must each be present and may each be any admitted JSON value. An absent top-level target is invalid; absence is modeled only at object members. No mode, collection, filenames, paths, operation list or external-reference field is recognized.

Object patches preserve unmentioned fields, remove named fields whose patch value is null and recursively transform other named values. If the current target is not an object, object processing starts from an empty object. Removing an absent member is harmless. Other patch types replace the whole current value, including array, null, false and zero. Arrays are not concatenated or patched by index; null inside a replacement array stays null. Empty object patch preserves an object but transforms a scalar/array/null into an empty object. Nested absent-object patches containing only a deletion still create the nested empty object. Existing target null is preserved when unmentioned.

Member names compare exact code points, with no normalization, case folding, trimming, tilde or percent decoding. Names such as slash, `~1`, percent text, empty text, NUL and composed/decomposed accents are ordinary keys. JSON escapes are decoded once by the JSON parser. A list that resembles RFC6902 operations is an ordinary replacement array; an object member named op/path is ordinary data. No reference/path language is interpreted. Reports must declare this single merge-value representation.

The model operates on values rather than source text. Reject duplicate decoded keys globally and do not promise source whitespace/key-order/numeric-spelling preservation. For deterministic reporting, JSON output uses ASCII escaping, sorted object keys, compact separators and one newline. Lists retain order. The profile supplies its own typed `changed` comparison: strings/integers/booleans/null require the same exact type/value; lists compare element order recursively; dicts compare exact names/values without considering insertion order. In particular false and integer zero differ. This is a lab report indicator, not a minimal-patch or authorization verdict.

Both caller target and patch remain unchanged. All report target/patch/result snapshots are detached from caller inputs and each other, even when native caller containers share acyclic subtrees. Use only admitted builtins for cloning, not arbitrary deepcopy/user hooks. Concurrent caller mutation and hostile interpreter/module tampering are outside the model.

## Exact input, native and result limits

Raw input limit:32768 bytes, strict UTF-8/no BOM/trailing text. Before json.loads, lexical gates cap container depth at8 including the envelope and numeric lexemes at32 characters. Reject fractions/exponents/nonfinite values, `-0`, unsafe integers outside ±9007199254740991 and malformed numeric grammar. Decoder hooks reject duplicate decoded object names at every level. These restrictions define an integer-only JSON subset, not RFC7396 requirements. Native parsed-object API cannot recover numeric spelling; document that difference.

Admit exact built-in dict/list/str/int/bool/None only, using type identity before any object operation. Keys must be exact strings. Reject active-ancestor cycles; count shared acyclic nodes at each logical occurrence. bool is separate from int. Reject surrogates and Unicode noncharacters; preserve other scalars including controls, default-ignorables, private-use and unassigned characters. No Unicode-version-dependent normalization/classification is needed.

Freeze these named resource limits before code:

| Scope | Value nodes | Containers | Text/key scalars each | Total text/key scalars | UTF-8 text/key bytes each / total |
|---|---:|---:|---:|---:|---:|
| Global native envelope |1026|129|1024|5120|4096 /20480|
| Target separately |512|64|128|2048|512 /8192|
| Patch separately |512|64|128|2048|512 /8192|
| Result separately |1024|128|128|4096|512 /16384|

A value root counts once; every object value and array element counts recursively. Keys count toward text totals, not value nodes. A container counts once per logical occurrence. The global walk includes envelope/schema/target/patch; its bounds precede field interpretation. Individual target/patch container depth is at most7, equivalent to8 including envelope; result standalone depth is at most7. Native aliases crossing target and patch are counted twice as separate logical occurrences. Invalid unknown shapes remain bounded globally before rejection. Guard all global text types/lengths before regex/set/equality access.

Result bounds allow the union of two admitted object trees. No merge operation can repeatedly duplicate arbitrary subtrees because there is one supplied patch, no copy operation or batch/sequence expansion. The conservative result1024-node/128-container limits exceed the tight worst-case union1023/127 (two object roots collapse); result depth cannot exceed maximum admitted source depth. These guards are defensive, not claims of reachable over-result-limit cases under current source bounds. Four-byte-per-scalar UTF-8 caps are redundant with admitted scalar rules; global known-envelope text is also below the global cap. Test feasible exact/over input boundaries and document inaccessible guard states; do not manufacture unreachable mutants as primary evidence.

Recursive work and cloning must remain bounded by the admitted tree sizes/depth. Validate both full trees, including values destined for deletion/replacement, before transformation or unknown-schema classification. Full common admission precedes schema support; invalid/limit input wins over unsupported. After support classification, transform into private builtins, validate the result and serialize the complete report before opening an output file or emitting stdout.

## Report, output and error contract

Exact top-level report fields proposed for freeze: profile, representation (`merge-patch-value`), assumption (`synthetic supplied values; no resource modification or authorization verdict`), limits, target, patch, result, result_type and changed. Limits use one frozen dictionary of all input/global/target/patch/result/output/numeric bounds. result_type is object/array/string/integer/boolean/null. Snapshots are admitted values, not source byte preservation. No mutation trace, diff operation list, JSON Pointer interpretation or external evidence fetch is added.

ASCII JSON cap:65536 bytes including newline, checked before delivery. A planned genuine amplification case has disjoint target keys t00–t31 and patch keys p00–p31, each value60 supplementary scalars. Each source has2016 text/key scalars and7776 UTF-8 text/key bytes; the combined result has4032/15552. The literal-UTF-8 envelope fits32768 raw bytes, while target+patch+result ASCII snapshots alone exceed64KiB. Measure exact report bytes after implementation. Do not encode this input as ASCII escapes that already exceed raw-input admission. This is one-pair report amplification, not a claim of recursive exponential merge growth.

Exit0: complete report, changed false. Exit1: complete report, changed true. Exit2: invalid/resource/I/O/delivery failure. Exit3: fully admitted common shape with unknown schema. Fixed diagnostic JSON is exactly status error or unsupported plus reason, ending in newline. Reasons: `invalid input`, `resource limit`, `unsupported schema`, `invalid command arguments`, `I/O or output delivery failed`. Within invalid/limit category ties need no priority promise; all common admission failures beat schema/merge decisions. No partial report on logical validation/serialization failure.

CLI accepts a single regular envelope input file and an optional exclusive fresh output file. Output presence uses explicit None checks, not truthiness. No target file is modified; target is a value in the envelope. Bounded pre/open/post metadata checks, alias/hardlink prevention, checked short/write/flush/close handling, help delivery and dirty/both-failing-sink sanitization reuse reviewed owned patterns. stdout is report-only; diagnostics never echo documents, filenames or exception detail. Actual closed-pipe regression must guard interpreter exit120. Physical I/O failures can leave partial stdout or a partial newly created output; no atomic/race-containment claim.

## Threat model and non-goals

Untrusted synthetic encoded/native data may exploit permissive JSON defaults, duplicate fields, deep structures, huge numeric tokens, Unicode/member ambiguity, type/subclass/metaclass hooks, native cycles/alias amplification, mutation/alias leaks and escaped report amplification. Exact-type identity, full pre-admission, bounded logical counts/depth, private cloning and pre-delivery output checks address these within the lab. Reports intentionally include synthetic input/result values. Resource-change authorization and inappropriate deletion are application decisions outside the standard and this model.

Exclude actual file/configuration/remote-object patching, services/HTTP PATCH/API calls, real/private data or credentials, filesystem target traversal, schema/reference resolution, JSONPath/eval, RFC6902 operations, merge sequences, diff/minimal patch generation, normalization, installs, new repository, publication or spending. Hostile filesystem races, concurrent caller mutation, production identity/access policy, general floating-point JSON and complete conformance remain outside scope. Python3.13.7/Windows is the initial observed test target only.

## Independent expectations and mutants

Before runtime code, hand-specify original synthetic target/patch/result triples, changed/type values, complete reports and fixed diagnostics/statuses; hash the fixture/contract. Use mechanical JSON formatting only, never a resolver/merge implementation to generate expected results. Do not copy RFC/upstream vectors unless exact license/notices/provenance are reviewed first; preferred cases are original.

Required distinctions for the original oracle set:

- Member-null deletion from existing false/zero/null versus deleting absent member; preserve unmentioned null; false→zero and zero→false are changed.
- Root null, false, zero, string and empty/replacement arrays versus member-null behavior; retain null array elements and null fields in object values inside a replacement array, without recursively treating array contents as patches.
- Object patch on scalar/array/null and empty object patch; preserve empty target object; nested absent object containing a null deletion creates empty object.
- Keep unrelated siblings through a nested update; replace arrays wholly; a list resembling operations stays an array; op/path object names stay data.
- Exact composed/decomposed/empty/slash/tilde/percent/NUL keys; deterministic sorted output without normalization.
- Native shared subtrees/cross-source aliases, caller/result snapshot mutations, subclass/metaclass hooks and cycles.
- Full unselected/deleted-branch validation; escaped duplicate keys; late malformed patch with unknown schema beats unsupported; valid common unknown schema alone is unsupported.
- Feasible exact/over bytes/depth/nodes/containers/scalars/number bounds, genuine output overflow, fresh/empty/existing/alias paths and all physical delivery failures.

Five targeted semantic mutants: retain null as a field instead of deleting; concatenate arrays instead of replace; preserve scalar target when object patch is applied; normalize member names; return an input/patch alias instead of detached result. Add a separate output-cap mutant if the measured genuine amplification fits the weaker cap. Each must fail an independent assertion, not import/syntax error, in a fresh isolated copy with original hashes unchanged. Secondary idempotence checks may complement fixed oracles but cannot replace them. No mutation is applied to existing files/resources or upstream source.

## Ordered stages and definitions of done

1. Contract/fixtures: after approval, freeze exact limits/report fields/status/priority and complete original independent expectations before runtime code. Review source facts, manual examples and any license obligations; hash original bytes. Done: sufficient fixed oracle coverage and unchanged source provenance.
2. Admission/model: implement lexical/raw/native bounds, exact types/global logical counting and pure merge/detached report/typed changed indicator. Done: focused independent expected cases, full admission ordering, caller preservation and hook/cycle/alias regressions pass. Depends on1.
3. Checked CLI/demo: bounded regular input/exclusive output, ASCII report and original mixed synthetic cases. Done: all exit classes, help/empty/fresh/dirty/both-failing/close/real-pipe/hardlink cases, measured overflow and no source modification pass. Depends on2.
4. Verification/review: full normal/-O suites and optimized children, meaningful assertion mutants, compile, installed runtime/demo Bandit, ECC self-review/fixes/affected rechecks, exact source/evidence receipt and targeted secret-signature scan. Done: complete raw outcomes and limits, no ignored actionable findings or false independent-review claims. Depends on3.
5. Documentation/handoff: README problem/demo/architecture/setup/security/limitations/checks/learning, original license/attribution/AI disclosure, STATE/DECISIONS/LEARNING/REVIEW/VALIDATION and verified vault milestone. Done: fresh receipt hashes match current files, frozen original fixtures intact, coordinator-ready local handoff. Depends on4. Git/hosted security baseline is excluded by no-new-repository scope; future repository work needs authorization.

No runtime dependencies or new checker installation. Existing local Ollama was used once for bounded public learning labels, with corrections preserved; Codex owns the consequential semantics/security plan. No remote-worker checks/inference are needed for local-only scope. Avoid redundant suite runs after documentation-only updates; rerun affected checks after actual changes.

## Approved04:49 addendum

Coordinator SUCCESSORS.md “Two plan approvals and SemVer correction acceptance” approves stages1–5 after actual source/capture/vault review. Freeze at least32 FULL independent original reports and fixed invalid/unsupported/output-limit diagnostics before core. Cover all reviewed null/root/array/object/nested-null/name/typed equality/order/detachment semantics. Exact identity precedes caller hooks/equality/hash/iteration; validate complete supplied branches before schema/merge, including data that will disappear. Preserve every plan bound. Measure the genuine planned disjoint32+32-key supplementary-scalar case; if admitted and exceeding64KiB, require cap-weakening assertion mutant in addition to five semantic mutants. Any discrepancy is a review gate; no seam/exponential or unreachable-result-overflow claim. Normal/-O actual checked CLI, ECC/SAST/source/mutation receipts/docs/license/AI/learning/vault required. No new repository, actual resource modification, upstream execution/adoption/install or external action.
