# Fuentes normativas argentinas · Conectores MCP

Repositorios de la comunidad que conectan claude-for-legal directamente
con las fuentes oficiales argentinas. Reemplazan los conectores originales
del repositorio base (Westlaw, CourtListener, Everlaw) para práctica local.

Los conectores son la segunda capa del sistema. Los perfiles funcionan
sin ellos usando el perfil de práctica como única configuración.
Con los conectores, el sistema consulta fuentes primarias automáticamente
sin que el abogado tenga que pegar el texto de la norma en la sesión.

Compatible con cualquier cliente MCP estándar (Claude, OpenCode, u otros).
Los conectores que exponen endpoint público (URL) no requieren instalación local.
Los que usan `uvx` requieren Python con uv instalado.
Los que se instalan manualmente desde GitHub requieren configurar `claude_desktop_config.json` y, según el conector, dependencias adicionales (Python, Chrome, chromedriver).

---

## Cómo verificar que un conector está activo antes de usarlo

Los conectores de esta lista son proyectos de la comunidad sin mantenimiento
garantizado. Antes de depender de un conector en una sesión de trabajo:

1. En Claude.ai: ir a Settings > Integrations y verificar que el conector
   figura como activo. Si no aparece o figura inactivo, no está disponible.
2. En Claude Code: ejecutar `mcp list` para ver los conectores activos.
3. Hacer una consulta de prueba mínima antes de la consulta real.
   Si el conector responde con el texto correcto, está activo. Si devuelve
   error o no responde, aplicar el fallback correspondiente.

**Si un conector no responde:** no intentar la misma consulta dos veces.
Aplicar el fallback de la tabla de abajo y registrar en la sesión que el
conector no estaba disponible.

### Tabla de fallback por conector

| Conector | Función | Fallback si no responde |
|---|---|---|
| 1 - Ansvar (InfoLEG) | Texto de normas nacionales | infoleg.gob.ar acceso directo |
| 2 - voftec (normas PBA) | Legislación provincial PBA | normas.gba.gob.ar acceso directo. Si `verificar_vigencia` devuelve resultado anómalo, verificar contra Boletín Oficial PBA. |
| 3 - juba-mcp (JUBA/SCBA) | Jurisprudencia PBA | juba.scba.gov.ar acceso directo |
| 4 - saij-mcp (SAIJ) | Jurisprudencia + legislación + doctrina + dictámenes | saij.gob.ar acceso directo |
| 5 - csjn-mcp (CSJN) | Fallos CSJN | sj.csjn.gov.ar acceso directo |
| 6 - juscaba-mcp (JUSCABA) | Jurisprudencia fueros nacionales CABA | jusbaires.gob.ar acceso directo |
| 7 - joaquinescalante23/saij-mcp | SAIJ alternativo con grafo legal y OCR | saij.gob.ar acceso directo |
| 8 - Psflores (PJN/CABA) | Jurisprudencia fueros nacionales | pjn.gov.ar acceso directo |
| 9 - guidobonomini | Análisis semántico / glosario | Operar con glosario del CLAUDE.md; calidad terminológica puede bajar |
| 10 - Tesauro SAIJ | Vocabulario jurídico controlado | Usar terminología estándar CCCN y LCT directamente |
| 11 - BORA Oficial | Boletín Oficial de la República Argentina | boletinoficial.gob.ar acceso directo |
| 12 - scba-mcp-server | Sentencias y resoluciones de primera instancia PBA | sentencias.scba.gov.ar acceso directo |

Cuando se usa el fallback manual (pegar texto en sesión), indicar siempre
al inicio del texto pegado: fuente, fecha de consulta y URL de origen.

---

## Conectores disponibles

### 1. Ansvar-Systems/argentine-law-mcp

**Repositorio:** https://github.com/Ansvar-Systems/argentine-law-mcp
**Fuentes:** InfoLEG · SAIJ
**Función:** Devuelve el texto literal de normas nacionales argentinas sin
pasar por ningún modelo de lenguaje. Consulta directa a InfoLEG.
**Estado al mayo 2026:** activo según última verificación. Confirmar antes de usar.

Casos de uso:
- Verificar el texto actual de un artículo del CCCN, LCT, LDC u otra norma nacional
- Confirmar si una norma fue modificada o derogada
- Obtener el texto de una ley especial sin buscarlo manualmente

Limitaciones:
- Solo normas nacionales (no provinciales)
- No incluye jurisprudencia
- No realiza análisis: devuelve texto literal

**Fallback:** infoleg.gob.ar · acceso directo sin conector.

---

### 2. voftec/normativapba-mcp

**Repositorio:** https://github.com/voftec/normativapba-mcp
**URL directa (Claude.ai):** https://normativapba-mcp.vercel.app
**Fuente:** normas.gba.gob.ar (Sistema de Información Normativa "Malvinas Argentinas" - Subsecretaría Legal y Técnica de PBA)
**Función:** Conector para legislación provincial de la Provincia de Buenos Aires.
Accede en tiempo real a normas.gba.gob.ar: leyes, decretos, resoluciones y
disposiciones PBA desde 1813 hasta la actualidad. Verifica vigencia, extrae
articulado y construye árboles de dependencia normativa.
**Instalación:** conexión directa vía URL en Claude.ai (Settings → Integrations → Add MCP Server → pegar la URL) sin necesidad de Node.js ni uvx. También instalable vía npx para Claude Code / Claude Cowork.
**Estado al mayo 2026:** verificado activo. Probado con búsqueda, texto completo y verificación de vigencia.

Herramientas disponibles:

| Herramienta | Función |
|---|---|
| `buscar_normativa` | Búsqueda de normas PBA por parámetros exactos |
| `verificar_vigencia` | Comprueba si la norma está vigente o fue derogada |
| `obtener_articulo` | Extrae un artículo específico |
| `obtener_texto_norma` | Descarga el texto íntegro de la norma |
| `alcance_normativo` | Informa la jurisdicción y metadatos del conector al LLM |
| `exportar_norma` | Genera Markdown estructurado con Frontmatter YAML |
| `relacionar_normativa` | Árbol de dependencias: qué deroga, qué modifica, qué reglamenta |
| `buscar_por_semantica` | Búsqueda por concepto con expansión de sinónimos |
| `mapa_normativo_tema` | Árbol jerárquico (Leyes → Decretos → Resoluciones) sobre un tema |

Casos de uso:
- Verificar texto y vigencia de normas provinciales PBA sin acceso manual al portal
- Obtener el articulado exacto de una ley o decreto PBA para citar en un escrito
- Construir el mapa normativo de un tema (ej. contratación pública PBA, procedimiento administrativo provincial)
- Detectar si una norma PBA fue modificada o derogada y por cuál

Limitaciones:
- Solo normas provinciales PBA (no normas nacionales ni de otras provincias)
- Instalación vía npx requiere Node.js; la conexión directa vía URL no tiene ese requisito
- Nota operativa (npx): el README documenta la necesidad de deshabilitar validación SSL
  (`NODE_TLS_REJECT_UNAUTHORIZED: 0`) para resolver certificados vencidos en el
  portal gubernamental; evaluar según política de seguridad del entorno
- **Limitación crítica - `verificar_vigencia`:** la herramienta reproduce el estado de vigencia
  tal como está cargado en `normas.gba.gob.ar`, incluyendo sus errores. Caso conocido y
  reportado: la Ley 11.922 (CPP Bonaerense, 1997) figura en el portal como derogada por la
  Ley/Decreto-ley 9032 (1978), cuando la relación es inversa. `verificar_vigencia` es un
  primer filtro, no una fuente definitiva. Ante resultados de derogación anómalos, verificar
  contra el Boletín Oficial PBA o el texto actualizado disponible en el portal.
  El error fue reportado al mantenedor del conector y a la Subsecretaría Legal y Técnica de PBA.

**Fallback:** normas.gba.gob.ar acceso directo sin conector.

---

### 3. juba-mcp (Hernán Caravario)

**Instalación:** `claude mcp add juba-mcp -- uvx juba-mcp`
**Fuente:** https://juba.scba.gov.ar/ (SCBA - Suprema Corte de Justicia de la Provincia de Buenos Aires)
**Función:** Búsqueda de jurisprudencia de la SCBA y cámaras de apelación provinciales PBA vía JUBA.
**Viabilidad técnica:** HIGH - interfaz AJAX sin protección antibot significativa; compatible con scraping estándar.
**Estado al mayo 2026:** verificado publicado. Comando de instalación confirmado en página del autor.

Casos de uso:
- Buscar jurisprudencia SCBA por materia, sala o período
- Verificar criterio de cámaras de apelación PBA antes de citar en un escrito
- Rastrear evolución jurisprudencial provincial sobre un instituto

Cobertura JUBA (Acuerdo 4011 / Resolución RP 1651/24):
- Desde marzo 2025: Cámaras de Apelación provinciales y Tribunal de Casación Penal
- Desde junio 2025: juzgados de primera instancia civiles, laborales y contencioso administrativos

Limitaciones:
- Solo jurisprudencia PBA; no cubre fueros nacionales ni CSJN
- Los resultados deben verificarse antes de citar

**Fallback:** juba.scba.gov.ar acceso directo sin conector.

---

### 4. saij-mcp (Hernán Caravario)

**Instalación:** `claude mcp add saij-mcp -- uvx saij-mcp`
**Fuente:** https://saij.gob.ar/ (Sistema Argentino de Información Jurídica - Ministerio de Justicia)
**Función:** Búsqueda en SAIJ de jurisprudencia, legislación, doctrina y dictámenes. Acceso a más de 330.000 documentos jurídicos.
**Viabilidad técnica:** HIGH
**Estado al mayo 2026:** verificado publicado. Comando de instalación confirmado en página del autor.

Casos de uso:
- Buscar jurisprudencia de todas las instancias indexadas en SAIJ
- Buscar doctrina y dictámenes en la misma operación
- Verificar legislación nacional con texto actualizado

Limitaciones:
- No cubre fuentes ajenas a SAIJ (CSJN directa, JUBA, PJN)
- Los resultados deben verificarse antes de citar

**Fallback:** saij.gob.ar acceso directo sin conector.

---

### 5. csjn-mcp (Hernán Caravario)

**Instalación:** `claude mcp add csjn-mcp -- uvx csjn-mcp`
**Fuente:** CSJN
**Función:** Búsqueda de fallos de la Corte Suprema de Justicia de la Nación.
**Viabilidad técnica:** HIGH
**Estado al mayo 2026:** verificado publicado. Comando de instalación confirmado en página del autor.

Casos de uso:
- Buscar doctrina de la CSJN por materia
- Verificar fallos antes de citar en recursos extraordinarios
- Rastrear evolución de criterio CSJN sobre un instituto

Limitaciones:
- Solo jurisprudencia CSJN; no cubre instancias inferiores
- Los resultados deben verificarse antes de citar

**Fallback:** sj.csjn.gov.ar acceso directo sin conector.

---

### 6. juscaba-mcp (Hernán Caravario)

**Instalación:** `claude mcp add juscaba-mcp -- uvx juscaba-mcp`
**Fuente:** Poder Judicial CABA / fueros nacionales con sede en CABA
**Función:** Búsqueda de jurisprudencia de fueros nacionales y locales con sede en CABA.
**Viabilidad técnica:** HIGH
**Estado al mayo 2026:** verificado publicado. Comando de instalación confirmado en página del autor.

Casos de uso:
- Buscar fallos de fueros nacionales (civil, comercial, laboral, penal) con sede en CABA
- Verificar criterio de salas antes de citar en escritos

Limitaciones:
- No cubre PBA ni CSJN
- Los resultados deben verificarse antes de citar

**Fallback:** jusbaires.gob.ar acceso directo sin conector.

---

### 7. joaquinescalante23/saij-mcp

**Repositorio:** https://github.com/joaquinescalante23/saij-mcp
**Fuente:** SAIJ (jurisprudencia, legislación, doctrina y dictámenes)
**Función:** Motor de investigación profunda en SAIJ con acceso a más de 330.000
documentos jurídicos. Único conector gratuito que cubre jurisprudencia, legislación,
doctrina y dictámenes en una sola herramienta, con navegación de grafo legal y
resolución directa de citas textuales.
**Estado al mayo 2026:** proyecto de la comunidad sin mantenimiento activo declarado.
Verificar estado antes de usar.

**Advertencia de infraestructura:** opera mediante ingeniería inversa de la API
pública de SAIJ (incluida una ruta no documentada oficialmente, `/suggest`).
Si SAIJ modifica su estructura, el conector puede romperse sin aviso previo.

Herramientas disponibles:

| Herramienta | Función |
|---|---|
| `saij_search_jurisprudencia` | Búsqueda avanzada de fallos y sentencias |
| `saij_search_legislacion` | Búsqueda de leyes, decretos y reglamentaciones |
| `saij_get_document` | Texto completo con OCR para PDFs escaneados históricos |
| `saij_get_related_documents` | Navega el grafo legal: normativa citada y fallos relacionados |
| `saij_get_document_section` | Extrae artículos o secciones específicas de códigos extensos |
| `saij_resolve_citation` | Convierte una cita textual ("Ley 24.240") en el documento |
| `saij_suggest_terms` | Autocompletado de terminología jurídica argentina |
| `saij_get_novedades` | Actualizaciones legales recientes en SAIJ |

Casos de uso:
- Navegar la red de citas entre un fallo y las normas que aplica (y viceversa)
- Resolver citas directas en el escrito: el sistema recupera el texto exacto
- Acceder a jurisprudencia histórica en PDF escaneado mediante OCR integrado
- Buscar doctrina y dictámenes en la misma operación que jurisprudencia

Limitaciones:
- Depende de infraestructura no oficial de SAIJ: mayor riesgo de rotura que conectores 1-6
- No cubre fuentes ajenas a SAIJ (CSJN directa, JUBA, PJN)
- No reemplaza al conector 1 (Ansvar) para verificación del texto oficial de normas nacionales

**Fallback:** saij.gob.ar acceso directo sin conector.

---

### 8. Psflores/Legal-MCP-Server-

**Repositorio:** https://github.com/Psflores/Legal-MCP-Server-
**Fuentes:** Poder Judicial de la Nación · Justicia CABA
**Función:** Búsqueda de jurisprudencia de fueros nacionales y CABA.
**Estado al mayo 2026:** proyecto de la comunidad sin mantenimiento activo declarado.
Verificar estado antes de usar.

Casos de uso:
- Buscar fallos por doctrina antes de citar en un escrito
- Verificar criterio de la sala en una materia específica

Limitaciones:
- No cubre PBA (SCBA ni cámaras de apelación provinciales)
- Los resultados deben verificarse antes de citar

**Fallback:** pjn.gov.ar · jusbaires.gob.ar acceso directo.

---

### 9. guidobonomini/argentina-law-mcp-server

**Repositorio:** https://github.com/guidobonomini/argentina-law-mcp-server
**Función:** Análisis semántico de documentos legales, glosario judicial
argentino, detección de riesgos calibrada para praxis local.
**Estado al mayo 2026:** proyecto de la comunidad sin mantenimiento activo declarado.
Verificar estado antes de usar.

Casos de uso:
- Análisis de contratos con terminología jurídica argentina nativa
- Corrección de terminología cuando el sistema genera términos de common law
- Consistencia terminológica en documentos largos

Limitaciones:
- No conecta a fuentes primarias oficiales
- Complementa al conector 1, no lo reemplaza

**Fallback:** operar con el glosario de terminología del CLAUDE.md argentino.

---

### 10. datos-justicia-argentina/Tesauro-Saij-de-Derecho-Argentino

**Repositorio:** https://github.com/datos-justicia-argentina/Tesauro-Saij-de-Derecho-Argentino
**Fuente:** SAIJ
**Función:** Vocabulario controlado para búsqueda jurídica. Mapea sinónimos,
términos preferidos y jerarquías conceptuales del derecho argentino.
**Estado al mayo 2026:** repositorio de datos estático; menor riesgo de caída
que los conectores de consulta en tiempo real.

Casos de uso:
- Mejorar la precisión de búsquedas jurisprudenciales
- Evitar que el sistema use términos de common law cuando existe equivalente argentino

Limitaciones:
- Es un vocabulario de referencia, no un conector a fuentes primarias
- No devuelve texto normativo ni fallos: solo estructura conceptual

**Fallback:** usar terminología estándar de CCCN, LCT y LDC directamente.

---

### 11. BORA Oficial (bora-mcp)

**URL directa (Claude.ai):** https://bora-mcp.vercel.app/api/mcp/sse
**Fuente:** boletinoficial.gob.ar (Boletín Oficial de la República Argentina)
**Función:** Consulta directa al BORA. Devuelve la portada del día, sumario completo
por fecha, texto verbatim de avisos por ID, nuevas sociedades (Segunda Sección)
y licitaciones públicas (Tercera Sección).
**Instalación:** conexión directa vía URL en Claude.ai (Settings → Integrations →
Add MCP Server → pegar la URL). Sin Node.js ni uvx.
**Estado al mayo 2026:** verificado activo. Probado con todas las herramientas disponibles.

Herramientas disponibles:

| Herramienta | Función |
|---|---|
| `obtener_portada` | Portada del día con links a PDFs firmados de las 4 secciones |
| `obtener_sumario_del_dia` | Sumario completo por fecha, agrupado por rubros |
| `obtener_detalle_aviso` | Texto verbatim de un aviso por sección, ID y fecha |
| `buscar_nuevas_sociedades` | Constituciones de S.A., S.R.L. y S.A.S. en la Segunda Sección |
| `buscar_licitaciones_publicas` | Licitaciones y contrataciones en la Tercera Sección con criterio y rango de fechas |
| `alcance_fuente` | Capacidades, fuentes y limitaciones del conector |
| `buscar_avisos` | Búsqueda de avisos por texto libre |
| `obtener_enlace_pdf` | Link directo al PDF firmado digitalmente de un aviso |
| `obtener_sumario_seccion` | Sumario de una sección específica para una fecha |

Casos de uso:
- Verificar el texto exacto de un decreto, resolución o disposición publicada hoy
- Consultar la portada del día para detectar normas relevantes por área
- Buscar la constitución de una sociedad y obtener el texto del acto constitutivo
- Rastrear licitaciones públicas por organismo o materia
- Confirmar si una norma fue publicada en el BORA en una fecha determinada

Limitaciones:
- Cubre exclusivamente el BORA nacional; no incluye boletines provinciales
- `buscar_nuevas_sociedades` indexa avisos de la Segunda Sección sin discriminar
  siempre por tipo de acto: puede retornar convocatorias a asamblea junto con constituciones.
  Cruzar el resultado con `obtener_detalle_aviso` para confirmar el tipo de acto
- No reemplaza al conector 1 (Ansvar) para verificar texto consolidado de una norma:
  el BORA devuelve la publicación original, no el texto con todas sus modificaciones

**Nota operativa:** para verificar vigencia, usar conector 1 (Ansvar) o conector 2
(voftec para normas PBA). El BORA confirma la publicación original y las normas
modificatorias individualmente, pero no consolida el texto.

**Fallback:** boletinoficial.gob.ar acceso directo sin conector.

---

### 12. FacundoEmanuel/scba-mcp-server

**Repositorio:** https://github.com/FacundoEmanuel/scba-mcp-server
**Fuente:** https://sentencias.scba.gov.ar/ (portal de sentencias de primera instancia PBA - distinto de JUBA)
**Función:** Scraper de sentencias y resoluciones de juzgados de primera instancia de PBA. Busca por organismo, rango de fechas y texto libre; devuelve el texto completo de cada documento y puede guardarlo en disco organizado por carpetas.
**Instalación:** manual desde repositorio. Requiere Python 3.9+, Chrome instalado localmente y chromedriver compatible. No tiene instalación por URL ni por uvx.
**Estado al mayo 2026:** proyecto de la comunidad, un solo commit. Verificar estado antes de usar.

Herramientas disponibles:

| Herramienta | Función |
|---|---|
| `listar_organismos` | Devuelve la lista de organismos disponibles (scraped en tiempo real del sitio) |
| `listar_tipos_registro` | Devuelve los tipos disponibles: sentencias / resoluciones |
| `buscar_documentos` | Busca y devuelve el texto completo de los documentos encontrados |
| `guardar_documentos_en_disco` | Guarda los resultados como `.txt` organizados por organismo y tipo |
| `cerrar_navegador` | Libera el Chrome al terminar la sesión |

Casos de uso:
- Buscar resoluciones o sentencias de un juzgado de primera instancia PBA por texto libre y rango de fechas
- Armar un corpus de documentos de un organismo para análisis en sesión
- Complementar al conector 3 (juba-mcp): JUBA cubre SCBA y cámaras; este cubre primera instancia

Limitaciones:
- **Solo primera instancia:** no cubre JUBA (SCBA ni cámaras de apelación PBA). Para esos, usar conector 3.
- Requiere Chrome local: no funciona en entornos cloud ni en Claude.ai web. Solo para Claude Desktop o Claude Code en la máquina del abogado.
- Scraper con pausas aleatorias: sesiones largas (muchos documentos) pueden ser lentas.
- Un solo commit, sin tests, sin releases: mayor riesgo de rotura ante cambios del portal.

**Fallback:** sentencias.scba.gov.ar acceso directo sin conector.

---

## Tabla de decisión - qué conector usar

| Necesidad | Conector recomendado | Alternativa |
|---|---|---|
| Verificar texto de una norma nacional | 1 (Ansvar) | InfoLEG directo |
| Verificar texto de una norma provincial PBA | 2 (voftec) | normas.gba.gob.ar directo |
| Buscar jurisprudencia PBA (SCBA y cámaras) | 3 (juba-mcp) | juba.scba.gov.ar directo |
| Buscar jurisprudencia + doctrina + dictámenes | 4 (saij-mcp) | saij.gob.ar directo |
| Buscar fallos CSJN | 5 (csjn-mcp) | sj.csjn.gov.ar directo |
| Buscar jurisprudencia fueros nacionales CABA | 6 (juscaba-mcp) | jusbaires.gob.ar directo |
| Navegar grafo legal / resolver citas / OCR histórico | 7 (joaquinescalante23/saij-mcp) | saij.gob.ar directo |
| Buscar jurisprudencia PJN alternativa | 8 (Psflores) | pjn.gov.ar directo |
| Análisis semántico / terminología | 9 (guidobonomini) | Glosario CLAUDE.md |
| Mejorar búsquedas jurisprudenciales | 10 (Tesauro SAIJ) | SAIJ directo |
| Texto de normas publicadas en BORA / sociedades / licitaciones | 11 (BORA Oficial) | boletinoficial.gob.ar directo |
| Buscar sentencias/resoluciones de juzgados de primera instancia PBA | 12 (scba-mcp-server) | sentencias.scba.gov.ar directo |

**Combinaciones recomendadas:**

- **1 + 2:** práctica bonaerense completa. Normas nacionales (InfoLEG) + normas provinciales PBA.
- **1 + 3 + 4:** flujo de investigación completo para escritos en fuero provincial PBA. Norma nacional verificada + jurisprudencia PBA + doctrina SAIJ.
- **1 + 5 + 6:** recursos extraordinarios y escritos ante fueros nacionales. Norma verificada + CSJN + fueros nacionales CABA.
- **1 + 11:** verificación normativa completa. El 1 da el texto consolidado; el 11 confirma la publicación original y rastreala cadena de modificaciones por fecha.
- **11 + societario-CLAUDE.md:** due diligence societario. El 11 busca el acto constitutivo y modificaciones en el BORA; el perfil aporta la lógica de análisis LGS.
- **10 + 4:** el Tesauro normaliza la terminología antes de ejecutar la búsqueda en SAIJ.
- **1 + 9:** análisis de contratos. El 9 detecta terminología; el 1 verifica las normas citadas.
- **3 + 12:** cobertura complementaria de jurisprudencia PBA. El 3 cubre SCBA y cámaras vía JUBA (y desde junio 2025 también primera instancia civil, laboral y contencioso administrativo). El 12 cubre primera instancia vía sentencias.scba.gov.ar con búsqueda por texto libre y descarga de documentos completos, funcionalidad que JUBA no expone con la misma granularidad. Hay solapamiento parcial en primera instancia desde junio 2025: usar el 12 cuando se necesite texto completo del documento o búsqueda por palabra clave dentro del cuerpo de la resolución.

**Si dos conectores dan resultados contradictorios:**
Los conectores 1-6 acceden a fuentes primarias oficiales: en caso de contradicción
con cualquier otro conector o con el conocimiento base del sistema, prevalece
la fuente primaria. El conector 12 también accede a una fuente oficial
(sentencias.scba.gov.ar) pero es un scraper de mayor fragilidad técnica que 1-6:
si sus resultados contradicen al conector 3 (juba-mcp) sobre el mismo documento,
verificar directamente en el portal antes de proceder. Los conectores 9 y 10 son instrumentos auxiliares:
si contradicen una fuente primaria, reportar la discrepancia al abogado con el marcador:

```
[DISCREPANCIA ENTRE FUENTES: el conector [X] indica [A] / la fuente primaria
 indica [B]. Verificar directamente en fuente primaria antes de proceder.]
```

---

## Integraciones en seguimiento

Fuentes relevantes para la práctica argentina sin conector MCP verificado públicamente
al momento de esta actualización. Se documentan como objetivos de integración para
seguimiento o desarrollo por la comunidad.

| Nombre tentativo | Fuente | URL | Viabilidad técnica estimada | Estado |
|---|---|---|---|---|
| `bopba-mcp` | Boletín Oficial PBA | boletinoficial.gba.gob.ar | MEDIUM-HIGH - scraping de PDFs vía Cheerio, búsqueda por formulario | No verificado públicamente |
| `ptn-mcp` | PTN - Buscador de dictámenes | busquedadictamenes.ptn.gob.ar | HIGH - SPA React sobre Elasticsearch JSON API directa | No verificado públicamente |
| `tfn-mcp` | Tribunal Fiscal de la Nación | jurisprudenciatfn.mecon.gob.ar | HIGH - formulario HTTP POST simple, compatible con cheerio/axios | No verificado públicamente |
| `dppj-mcp` | DPPJ PBA - Personas Jurídicas | gba.gob.ar/dppj | MEDIUM-HIGH - sistema Tramix Web, scraping por legajo/expediente con rate limiting | No verificado públicamente |
| `bcra-deudores-mcp` | BCRA - Central de Deudores | bcra.gob.ar/bcrayvos/situacion_crediticia.asp | LOW - Cloudflare + reCAPTCHA v3, bloquea Vercel/AWS; inviable en entornos cloud serverless | No verificado públicamente |

Para contribuir con alguna de estas integraciones, abrí un PR en este repositorio
con el conector implementado y el estado verificado.

---

## Fuentes primarias oficiales (sin conector MCP)

Acceso directo por el abogado para verificación manual. Son la fuente de verdad
ante cualquier discrepancia con un conector.

| Fuente | URL | Uso principal |
|---|---|---|
| InfoLEG | infoleg.gob.ar | Texto oficial de normas nacionales |
| normas.gba.gob.ar | normas.gba.gob.ar | Texto oficial de normas provinciales PBA |
| SAIJ | saij.gob.ar | Jurisprudencia, doctrina, legislación provincial |
| PJN | pjn.gov.ar | Acordadas y jurisprudencia federal |
| CNACAF | cnacaf.gov.ar | Jurisprudencia contencioso administrativo federal y alzada tributaria |
| SCBA | scba.gov.ar | Jurisprudencia PBA - fuente primaria bonaerense |
| JUBA | juba.scba.gov.ar | Consulta de jurisprudencia PBA (SCBA + cámaras + primera instancia desde 2025) |
| Poder Judicial CABA | buenosaires.gob.ar/jusbaires | Jurisprudencia fuero local CABA |
| PTN | busquedadictamenes.ptn.gob.ar | Dictámenes - responsabilidad del Estado y empleo público |
| AAIP | argentina.gob.ar/aaip | Disposiciones de datos personales |
| IGJ | igj.gob.ar | Resoluciones societarias CABA |
| DPPJ | gba.gob.ar/dppj | Resoluciones societarias PBA |
| CNV | cnv.gov.ar | Normas y resoluciones mercado de capitales |
| BCRA | bcra.gov.ar | Normativa cambiaria y financiera |
| COMARB | comarb.gov.ar | Convenio Multilateral - Ingresos Brutos |
| TFN | jurisprudenciatfn.mecon.gob.ar | Jurisprudencia tributaria |
| Boletín Oficial PBA | boletinoficial.gba.gob.ar | Publicaciones oficiales PBA |

---

## Instalación de conectores MCP

**En Claude.ai (conexión directa vía URL):**
Para conectores que exponen endpoint público:
1. Ir a Settings → Integrations → Add MCP Server
2. Pegar la URL del endpoint (ej. `https://normativapba-mcp.vercel.app` para el conector 2)
3. Confirmar y verificar que el conector aparezca activo
4. Hacer una consulta de prueba antes de usar en sesión real

No requiere Node.js, Python ni configuración local.

**Con uvx (conectores de Caravario - conectores 3 a 6):**
Requiere Python con uv instalado (`pip install uv`).
```
claude mcp add juba-mcp -- uvx juba-mcp
claude mcp add saij-mcp -- uvx saij-mcp
claude mcp add csjn-mcp -- uvx csjn-mcp
claude mcp add juscaba-mcp -- uvx juscaba-mcp
```

**Manual desde GitHub (conector 12 - scba-mcp-server):**
Requiere Python 3.9+, Chrome y chromedriver compatibles.
```bash
git clone https://github.com/FacundoEmanuel/scba-mcp-server.git
cd scba-mcp-server
pip install mcp selenium
```
Agregar al `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "scba-sentencias": {
      "command": "python",
      "args": ["C:/ruta/al/proyecto/scba_mcp_server.py"]
    }
  }
}
```
En Mac/Linux usar ruta Unix. Reiniciar Claude Desktop después de guardar.

**En Claude Code / Claude Cowork:**
Agregar al archivo `.mcp.json` del proyecto o via configuración de MCP Servers.
Ver instrucciones detalladas en el README del repositorio de cada conector.

**Compatibilidad:** todos los conectores listados son compatibles con cualquier
cliente MCP estándar (Claude, OpenCode u otros) que soporte el protocolo MCP
sobre HTTP/SSE o stdio.

---

## Módulo de automatización de escritorio (macOS)

`macos-use` no es un conector a fuentes jurídicas sino una capa de automatización
de apps macOS. Se documenta aquí porque se instala como servidor MCP junto con
los conectores de fuentes.

**Solo aplica a:** Claude Code en Mac con macOS 13+. No aplica a Claude.ai web
ni a entornos Windows/Linux.

**Instalación en Claude Code:**
```bash
claude mcp add macos-use -- npx -y mcp-server-macos-use
```

Requiere permiso de Accesibilidad en el terminal. Ver instrucciones completas
en `argentina/macos-automation.md`.

**Casos de uso jurídicos:** portales judiciales sin API (PJN, MEJ, SCBA),
carga de escritos en sistemas de gestión, formularios de organismos administrativos
(IGJ, AFIP desktop, ANSES), adjuntar y enviar documentos generados por el sistema.

---

## Contribuciones

Si desarrollás un conector para una fuente listada en "Integraciones en seguimiento"
o para cualquier fuente provincial no cubierta, abrí un PR en este repositorio
para agregar la referencia a esta lista.

---

*Última actualización: mayo 2026*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
