# Receiving factory updates
This OS is an independent snapshot. Its original package hashes live in `_meta/forge-manifest.json` at the OS root.
Local changes belong to the recipient. Before an update, compare the old baseline, current file and incoming file.
Unchanged managed files can receive the new version with archived predecessors. A local change creates a conflict for review.
Unmanaged files and original data are never overwritten or deleted. Removed upstream files remain for owner review.
The factory deploy command defaults to a preview. Applying a package is separate from activating any runtime.
Do not hand-edit the generated manifest. It records deployed bytes, not the recipient's preferred content.
