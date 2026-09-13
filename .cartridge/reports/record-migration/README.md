# Central planning record migration

The manifest records original and relocated paths, hashes, source repository mappings and every original PRD/native planning frontmatter value. Original review-inputs.json files remain byte-for-byte unchanged. Their scores and round counts are historical; relocated PRDs are marked stale-after-migration and require current review before implementation. No product work is marked complete by this relocation.

Recovery snapshots are local task artifacts at `/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-record-migration.fbddr8pu`. Existing source-tree changes were preserved; this migration makes no Git commits or index changes.
