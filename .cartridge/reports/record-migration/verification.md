# Record migration verification

`python3 prd.ctg/.cartridge/scripts/check-records.py --migration` passes. All182 actual PRDs remain in their original alias scope, including180 reviewed inventory entries and two additional real records. Every active board and PRD names its source repository. Original PRD metadata, dependencies and lifecycle state are preserved apart from explicit repository mapping and the stale review marker. All385 imported work records and one question preserve their status, owner and claims. Review-input JSON files retain their exact original hashes.

All435 current native memo headers parse as YAML. Link verification found no new broken Markdown links;179 link failures already existed in the source census and remain recorded in the manifest for later source repair. Eleven legacy unquoted YAML reference fields were normalized when their targets became qualified.

Planning boards, workflows, templates, development-entry notes and native work/question records were removed from source cartridges. Superseded duplicate orchestration routines and the frozen-inventory validator were retired. Historical source facts about old boards remain in generic memory-store measurements and memo resolver citations; they are not executable planning dependencies. The archived upstream board remains separately owned and is excluded from automatic dispatch.

No product work is completed by moving its record. Historical scores are not renewed approval. No commits, Git index writes, pushes or claims were made by this migration. The coordinator verifies native service, memory and event integration separately.
