# Host requirements

Use a file-capable agent with authorized read/write access to the selected root and Python 3.10+. Generator, inventory, relocation, verification, sparse XLSX and search use the standard library. Embedded PDF/XLSX extraction optionally uses PyMuPDF (or pypdf) and openpyxl. DOCX/PPTX/plain text use standard-library parsing. Missing dependencies are per-format gaps.

`requirements-extraction.txt` lists optional parser packages. When installation is authorized and useful, select an isolated environment for the station:

```text
python -m venv <environment-folder>
<environment-python> -m pip install -r <skill>/requirements-extraction.txt
```

Discover the actual executable; syntax depends on the host. Do not assume an account, machine path, bundled runtime, browser or model. Core construction works without external connectors. Web/account tasks require the host's actual tools and owner authorization.

Keep the whole skill folder together. For Codex, place it in the configured skills directory. For another file-capable agent, provide SKILL.md explicitly and follow the host's own discovery mechanism. Nested blueprint skills are methods available by reading their entries; automatic discovery is unverified until tested on that host.

Fleet role cards describe responsibility and scoped behavior. Real delegation requires an available executor and authorization. One assistant can work sequentially through roles; it must not claim those are independently running agents. Activation evidence, model choice, mounts and access tests stay in the recipient OS.
