# OS Forge

Construye tu propio sistema operativo personal a partir de tus archivos, con una estructura ICM y un **agent fleet** para trabajar sobre empresas, proyectos, finanzas, salud, aprendizaje, viajes y conocimiento.

OS Forge coordina el proceso completo. [ICM Architect](assets/blueprint/00_System/Skills/icm-architect/SKILL.md) aporta el método de arquitectura y viene incluido con su licencia. [Agent Fleet](assets/blueprint/00_System/Skills/agent-fleet/SKILL.md) define coordinador, especialistas, contexto permitido, entregables, delegación y pruebas. Los demás skills se consultan según la tarea.

## Empezar

Descarga o clona el repositorio. Conserva esta carpeta completa, incluidos `SKILL.md`, `scripts`, `references`, `agents` y `assets`. En Codex, instálala como `os-forge` en el directorio de skills configurado; por defecto `~/.codex/skills/os-forge`. También puedes darle directamente la ruta de `SKILL.md` a un agente con acceso a tus archivos.

Para empezar sin ayuda de quien te lo compartió:

1. Guarda el paquete completo fuera de la carpeta donde crearás tu OS. Cada persona usa su propia carpeta privada y sus propias cuentas. Compartir este método no requiere compartir archivos personales.
2. Abre el paquete en un asistente que pueda leer y guardar archivos. Puedes indicarle la ruta completa de `SKILL.md` sin instalar nada primero. Si tu aplicación solo permite adjuntar archivos al chat, puede preparar una propuesta, pero no verificar una instalación en tu computador.
3. Elige una sola tarea que te sirva hoy y, si hace falta, uno o dos archivos poco sensibles. No necesitas reunir toda tu vida digital ni conectar cuentas para empezar.
4. Copia esta petición y sustituye la ruta y la tarea:

> Lee el SKILL.md de OS Forge y ayúdame a crear mi OS en «ruta de una carpeta privada nueva», separado del paquete. Mi primera tarea es «tarea concreta». Usa solo los archivos que te indique, mantén los originales donde están y guarda un resultado útil con sus fuentes. Empieza con este asistente; deja los demás roles preparados para cuando hagan falta. Comprueba que una sesión nueva pueda encontrar y continuar el trabajo. Si te falta acceso, dime qué pudiste verificar y cuál es el único paso que debo resolver.

Una primera versión está lista cuando encuentras una fuente, guardas un resultado útil y lo recuperas desde una sesión nueva. Los dominios vacíos y los roles sin activar pueden esperar.

Para una organización más amplia, puedes pedir:

> Usa $os-forge para crear mi OS en «ruta de mi carpeta». Organiza los originales dentro del ICM conservando copias de recuperación, extrae información útil e intégrala con referencias. Crea el agent fleet personal y los especialistas que mis actividades necesiten, con límites de contexto y reglas de delegación. Quiero seguir construyéndolo desde mi station.

Para una primera propuesta sin traslado, pide mantener los originales en sus rutas. Si ya tienes un OS, pide integrar el trabajo existente y procesar solo los nuevos archivos. No necesitas las mismas actividades que otra persona.

Necesitas un agente con acceso autorizado a tu carpeta y Python 3.10+. Consulta [dependencias opcionales](references/runtime.md) para PDF/Excel. Los ejemplos de comandos usan rutas simbólicas; el agente debe resolver las rutas reales.

## Qué recibes

- Una guía de entrada, mapas pequeños, contratos y plantillas.
- Originales organizados con inventario, backups y verificación cuando autorizas su traslado.
- Conocimiento con enlaces y localizadores de sus fuentes; búsqueda local.
- Un fleet personal con seis roles generales y especialistas por compañía cuando haya un trabajo concreto para ellos.
- Fichas de agentes con alcance, entradas, salidas, modelo/capacidad requerida, handoffs y estado de activación.
- Una biblioteca de métodos portables, incluido Agent Fleet, que se consultan según la tarea, y una cobertura clara de lo pendiente.

Un fleet puede usarse con un asistente o varios agentes si la plataforma lo permite. Las fichas preparadas no arrancan procesos autónomos. Fotos catalogadas no equivalen a fotos interpretadas; extraer cifras no confirma conciliación. Publicar, enviar, pagar, conectar cuentas o activar automatizaciones requiere su alcance propio.

## Compartir

Publica **solo esta carpeta neutral**. Los OS generados, sus originales, configuraciones, inventarios y backups deben vivir fuera del repositorio. Puedes crear un repositorio vacío en GitHub y subir esta carpeta con la interfaz web o tu herramienta Git. No publiques el taller que originó este paquete.

## Comprobar

```text
python -m unittest discover -s scripts -p "test_*.py"
```

Para la suite completa, instala también las dependencias opcionales de extracción. Los tests usan datos sintéticos en carpetas temporales. Las instrucciones del skill están en inglés y esta guía en español; los entregables usan el idioma del propietario. [Licencia y atribuciones](THIRD_PARTY_NOTICES.md).
