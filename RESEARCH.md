# JSON Merge Patch lab research

Date: 2026-10-05. Preserved research-stage assessment: initial04:31 authority covered research/plan only. Coordinator subsequently approved PLAN stages1–5 at04:49; current implementation/checks are in STATE/VALIDATION. No new repository, installation or third-party execution occurred.

## Recommendation and reuse

Build an original standard-library implementation of a small RFC7396 value-transformation profile. Keep RFC6902 operation-list patching outside this lab. The direct merge candidate is small and dependency-free but its mutating/aliasing API and broader CLI require wrapping; an original bounded model makes caller preservation and resource decisions explicit. This is a fit recommendation, not a safety certification.

A bounded workspace Python/Markdown search for RFC7396, JSON Merge Patch and merge_patch found no standalone matching model after exclusions for private evidence, dependencies, firmware and GLPI. Relevant vault filename search found pointer/canonicalization/Unicode notes but no merge-patch note. Read Home/Codex Integration and relevant pointer/canonicalization completion notes, plus the current pointer admission and CLI source. Reuse reviewed exact-type identity, bounded lexical parsing, duplicate-key admission, detached copying, fixed checked CLI delivery and receipt patterns as ideas after approval. Preserve prior labs/shared helpers and avoid a cross-lab runtime import. Searches were relevant/bounded, not exhaustive.

The connected GitHub repository-search endpoint failed with a transport error. Public primary-source search provided repository comparisons, and connected GitHub repository/tree/file/issue fetches worked for actual inspection. The unavailable search is disclosed rather than claimed successful. No Firecrawl account/inference or paid fallback was needed.

## Standards comparison

[RFC7396](https://www.rfc-editor.org/rfc/rfc7396.html), sections1–2,5 and AppendixA, defines Merge Patch at the JSON-value level. An object patch recursively updates fields, treating member null as deletion; a nonobject target begins as an empty object. A nonobject patch replaces the target wholesale, including arrays and root null. Missing deletion is harmless. Existing target null remains when unmentioned. It does not preserve textual whitespace, duplicate names or arbitrary number precision, and does not establish permission to modify a resource. Those limits support a supplied synthetic model only.

[RFC6902](https://www.rfc-editor.org/rfc/rfc6902.html), sections3–5, defines ordered add/remove/replace/move/copy/test operations using reference paths. It enables array editing, explicit stored null and precondition tests, while adding operation order, path existence, value equality, copy/move behavior and failure policy. That is a distinct larger contract; implementing both would obscure this lab's missing/null/object/array lesson. No HTTP/service/API request is proposed for either standard.

Both RFC copyright notices require IETF Simplified BSD text for extracted Code Components. The recommendation is original code and original hand-specified synthetic cases, not copied pseudocode, ABNF or published examples. Any later copied material needs exact notices/source binding first. This research does not establish complete conformance or an errata/security audit.

## Strongest merge candidate inspected

[OpenDataServices/json-merge-patch](https://github.com/OpenDataServices/json-merge-patch/tree/1c3ca78f44d922c6fd6b17e19a925003c5dcae8f), tree1c3ca78f44d922c6fd6b17e19a925003c5dcae8f. Read complete README, actual LICENSE, setup.py/setup.cfg, lib.py, tests.py, cli.py and CI workflow. Source version0.3.0, Python>=3.9, no runtime install requirements; imports use stdlib. Repo metadata nonarchived, last push2025-03-25T09:48:12Z. Activity alone is not continued-maintenance proof or a latest-release assertion.

The core recursively merges dicts, removes None members and returns a non-dict patch. It mutates target dicts and assigns/returns patch arrays/values without detaching them. isinstance/OrderedDict support is broader than exact built-in admission. create_patch and position/order extensions exceed proposed scope. Tests include published merge examples, null deletion, nested objects, whole arrays and OrderedDict behavior; they do not supply this lab's native hooks/cycles/resource/I/O contract. No upstream test was run.

The CLI uses ordinary JSON loads without duplicate/nonfinite/size admission, a None sentinel while accumulating file inputs and w+ output writes. These are observed API choices requiring a wrapper for this bounded lab; no vulnerability or installed behavior was reproduced. Actual setup.py installs a prewritten script. Connected issue13 reports Windows incompatibility; issue14 proposes console_scripts. Issues8/11 report historical0.2 description-file installation failures, whereas the inspected0.3.0 setup.cfg is blank. Do not attribute that historical configuration error to current source. No installation was attempted.

CI source runs unittest on Python3.9–3.13, Ubuntu, push/PR, with editable installation and mutable checkout/setup-python version tags. No current CI pass, dependency advisory audit or Scorecard result was checked. Actual LICENSE is BSD-3-Clause, copyright Open Data Services Coop2015; copying source/tests requires retained notice, conditions/disclaimer and nonendorsement terms. Recommend original build rather than adoption/fork.

## Operation-list alternative inspected

[stefankoegl/python-json-patch](https://github.com/stefankoegl/python-json-patch/tree/d8e1a6e244728c04229d601bc9a384d9b034c603), treed8e1a6e244728c04229d601bc9a384d9b034c603. Read README/LICENSE/setup.py/requirements.txt/workflow; inspect actual apply/test/copy branches and corresponding tests from captured full files. Source1.33, runtime jsonpointer>=1.9 with an open dependency range; metadata nonarchived, last push2026-06-18T06:43:20Z. Actual license is BSD-3-Clause; preserve notices for any adoption.

apply defaults to deepcopy and sequential operations, with optional in_place=True. Tests distinguish copied/same-instance application and object/array operations. TestOperation uses Python value inequality and reports supplied values in failures; generic deepcopy and custom pointer classes require a separate bounded/type/diagnostic review. The workflow uses mutable action tags and an older Python2.7/3.7–3.11 matrix; its coverage command names jsonpointer despite the jsonpatch project. This is configuration inspection, not a reproduced CI failure or complete audit. Only selected evaluator/test branches were reviewed; the broader diff/operation engine was not exhaustively assessed. It is outside the recommended single-profile scope.

## Capture and worker evidence

Fifteen private candidate files were saved with original licenses. Every UTF-8 capture matched its inspected Git blob identity; byte lengths and SHA256 are in .private/research/capture-hashes.json, repository/ref bindings in capture-bindings.json. Capture integrity is not authentication or code safety. Captured third-party code was not executed/adopted and is not relicensed by any future lab license.

One bounded loopback Ollama draft supplied learning labels; returned four rather than three, with one ambiguous label. Reviewed corrections are preserved. No remote inference, new billing, install or provider probe. Codex retains standards/security/contracts/review. The concrete PLAN was approved at04:49 after the research handoff; the approval/addendum is recorded there.
