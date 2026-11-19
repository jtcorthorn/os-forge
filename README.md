# OS Forge

Build and run a personal operating system around the way you work. OS Forge proposes a structure inspired by my own JT OS, then adapts it to your files, projects, businesses and routines. It includes playbooks for maintaining the OS and assigning work to AI assistants as it grows.

Built on Jake Van Clief’s [ICM Architect](https://github.com/RinDig/icm-architect). OS Forge includes the [method](assets/blueprint/00_System/Skills/icm-architect/SKILL.md) and its [MIT license](assets/blueprint/00_System/Skills/icm-architect/LICENSE).

## Start here

Give your assistant the link to this repo and copy this request:

> Use OS Forge from https://github.com/jtcorthorn/os-forge to help me build my own OS. Show me the structure you propose and ask the questions needed to adapt it. At the end, leave me a short guide to using and maintaining my OS.

The assistant starts by proposing areas such as projects, businesses, travel and a library. Tell it what to keep, add or rename, what already works, who can access each area and the first task you want to do. Your OS lives in a separate folder under your control.

Use an assistant that can read the full repo and write to your chosen folder. If your assistant cannot read the repository from the link, clone it and point the assistant at its [SKILL.md](SKILL.md). For Codex skill discovery, place the complete folder under `~/.agents/skills/os-forge` or a project’s `.agents/skills/os-forge`. The core scripts use Python 3.10+. [Runtime requirements](references/runtime.md)

## What you get

- A map of your own areas and an `EMPIEZA_AQUI.md` guide in your language.
- Source-linked knowledge and a route for bringing in new material. Originals stay where they are unless you ask Forge to reorganize them.
- The [maintenance playbook](assets/blueprint/00_System/Skills/os-maintenance/SKILL.md) to check routes, handoffs and recovery.
- The [Agent Fleet playbook](assets/blueprint/00_System/Skills/agent-fleet/SKILL.md) to use a general assistant and add dedicated roles when the work calls for them.

## Guía breve en español

> Usa OS Forge desde https://github.com/jtcorthorn/os-forge para ayudarme a construir mi propio OS. Muéstrame primero la estructura que propones y hazme las preguntas necesarias para adaptarla. Al terminar, déjame una guía breve para usar y mantener mi OS.

Abre una carpeta privada en un asistente con acceso a archivos. Dile qué áreas te sirven, qué carpetas ya funcionan, qué vas a compartir y cuál es tu primera tarea. Forge te deja un mapa, una guía de uso y los playbooks para mantener el OS y distribuir responsabilidades. Empieza con los archivos que necesitas para esa tarea.

## Verify the repository

```text
python -m unittest discover -s scripts -p "test_*.py"
```

For the full suite, install the optional extraction dependencies. Tests use synthetic data in temporary folders. [License and credits](THIRD_PARTY_NOTICES.md).
