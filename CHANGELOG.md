# Changelog

## v0.7.2 - 2026-06-21

- Added `data/liuren_case_samples.json` with separate Da Liu Ren and Xiao Liu Ren schema fixtures.
- Added `liuren_case_samples` to generated data, backend search, local search, CLI query, and the "六壬资料" workbench view.
- Marked Liuren samples as non-accuracy fixtures with zero scoring so they cannot inflate prediction metrics.
- Expanded validation, smoke tests, function tests, predeploy checks, and public docs for the Liuren sample layer.

## v0.7.1 - 2026-06-21

- Added `data/liuren_case_schema.json` with shared Liuren fields plus separate Da Liu Ren and Xiao Liu Ren chart branches.
- Added `/api/liuren-case-schema` and a searchable `liuren_case_schema` backend kind while keeping `/api/case-schema` Liuyao-only.
- Surfaced Liuren case schema metadata in the "六壬资料" workbench view and CLI query path.
- Expanded validation, smoke tests, function tests, and predeploy checks for the new Liuren case contract.

## v0.7.0 - 2026-06-21

- Added the first Da Liu Ren / Xiao Liu Ren content layer with `data/liuren_terms.json` and `data/liuren_structures.json`.
- Added a "六壬资料" workbench view and backend search kinds for `liuren_terms` and `liuren_structures`.
- Added Liuren public sources and open-source project references while keeping Da Liu Ren and Xiao Liu Ren separated.
- Expanded validation, smoke tests, function tests, and predeploy checks for the new Liuren layer.

## v0.6.0 - 2026-06-21

- Added the first Qi Men Dun Jia content layer with `data/qimen_terms.json` and `data/qimen_structures.json`.
- Added a "奇门资料" workbench view and backend search kinds for `qimen_terms` and `qimen_structures`.
- Added Qimen public sources and open-source project references while keeping interpretation rules out of the Liuyao rule layer.
- Expanded validation, smoke tests, function tests, and predeploy checks for the new Qimen layer.

## v0.5.0 - 2026-06-21

- Added the first Zi Wei Dou Shu content layer with `data/ziwei_terms.json` and `data/ziwei_structures.json`.
- Added a "紫微资料" workbench view and backend search kinds for `ziwei_terms` and `ziwei_structures`.
- Added Zi Wei public sources and a foundation document while keeping interpretation rules out of the Liuyao rule layer.
- Expanded local validation, smoke tests, function tests, and predeploy checks for the new Zi Wei layer.

## v0.4.0 - 2026-06-21

- Added a lightweight multi-system roadmap for Liuyao, Zi Wei Dou Shu, Qi Men Dun Jia, and Da/Siao Liu Ren.
- Added `data/systems.json` and a "体系总览" workbench view.
- Kept the project on the existing static frontend plus thin Netlify Functions architecture to avoid framework bloat.
- Updated README and source notes to present the project as a broader professional knowledge workbench while clearly marking Liuyao as the first deep implementation.

## v0.3.1 - 2026-06-21

- Added three retrospective sports calibration cases with official result sources.
- Clarified that retrospective calibration samples do not count toward real prediction accuracy.
- Updated Netlify builds to regenerate knowledge-base data during deploy.
- Added handler-level Netlify Function tests and generated-asset sync checks.
- Removed local absolute runtime paths from public documentation.
- Published the project to GitHub and documented the current remote state.

## v0.3.0 - 2026-06-21

- Added 旬空 calculation by day ganzhi.
- Added month/day branch relation labels in the Liuyao chart engine.
- Added event accuracy case data and scoring documentation.
- Added GitHub-ready CI workflow and versioning notes.

## v0.2.0

- Added automatic hexagram, palace, six spirits, six relatives, shi/ying, and hidden-god hints.

## v0.1.0

- Built the local-first Liuyao knowledge base, static workbench, Netlify functions, and structured data checks.
