# OS Forge

Construye tu propio sistema operativo personal a partir de tus archivos, con una estructura ICM y un **agent fleet** para trabajar sobre empresas, proyectos, finanzas, salud, aprendizaje, viajes y conocimiento.

OS Forge coordina el proceso completo. [ICM Architect](assets/blueprint/00_System/Skills/icm-architect/SKILL.md) aporta el método de arquitectura y viene incluido con su licencia. [Agent Fleet](assets/blueprint/00_System/Skills/agent-fleet/SKILL.md) define coordinador, especialistas, contexto permitido, entregables, delegación y pruebas. Los demás skills se consultan según la tarea.

## Empezar

Descarga o clona el repositorio. Conserva esta carpeta completa, incluidos `SKILL.md`, `scripts`, `references`, `agents` y `assets`. En Codex, instálala como `os-forge` en el directorio de skills configurado; por defecto `~/.codex/skills/os-forge`. También puedes darle directamente la ruta de `SKILL.md` a un agente con acceso a tus archivos.

Prueba una petición como esta, sustituyendo la ruta:

> Usa $os-forge para crear mi OS en «ruta de mi carpeta». Organiza los originales dentro del ICM conservando copias de recuperación, extrae información útil e intégrala con referencias. Crea el agent fleet personal y los especialistas que mis actividades necesiten, con límites de contexto y reglas de delegación. Quiero seguir construyéndolo desde mi station.

Para una primera propuesta sin traslado, pide mantener los originales en sus rutas. Si ya tienes un OS, pide integrar el trabajo existente y procesar solo los nuevos archivos. No necesitas las mismas actividades que otra persona.

Necesitas un agente con acceso autorizado a tu carpeta y Python 3.10+. Consulta [dependencias opcionales](references/runtime.md) para PDF/Excel. Los ejemplos de comandos usan rutas simbólicas; el agente debe resolver las rutas reales.

## Qué recibes

- Una guía de entrada, mapas pequeños, contratos y plantillas.
- Originales organizados con inventario, backups y verificación cuando autorizas su traslado.
- Conocimiento con enlaces y localizadores de sus fuentes; búsqueda local.
- Un fleet personal con seis roles generales y especialistas por compañía cuando haya un trabajo concreto para ellos.
- Fichas de agentes con alcance, entradas, salidas, modelo/capacidad requerida, handoffs y estado de activación.
- Una biblioteca de 19 métodos portables, incluido Agent Fleet, y una cobertura clara de lo pendiente.

Un fleet puede usarse con un asistente o varios agentes si la plataforma lo permite. Las fichas preparadas no arrancan procesos autónomos. Fotos catalogadas no equivalen a fotos interpretadas; extraer cifras no confirma conciliación. Publicar, enviar, pagar, conectar cuentas o activar automatizaciones requiere su alcance propio.

## Compartir

Publica **solo esta carpeta neutral**. Los OS generados, sus originales, configuraciones, inventarios y backups deben vivir fuera del repositorio. Puedes crear un repositorio vacío en GitHub y subir esta carpeta con la interfaz web o tu herramienta Git. No publiques el taller que originó este paquete.

## Comprobar

```text
python -m unittest discover -s scripts -p "test_*.py"
```

Para la suite completa, instala también las dependencias opcionales de extracción. Los tests usan datos sintéticos en carpetas temporales. Las instrucciones del skill están en inglés y esta guía en español; los entregables usan el idioma del propietario. [Licencia y atribuciones](THIRD_PARTY_NOTICES.md).
