---
title: "Taller de Interpretación de Variantes"
description: Anota un genoma humano real con ClawBio en Google Colab. Sin instalación, sin terminal, sin experiencia previa.
---

# Taller de Interpretación de Variantes

<div class="tutorial-card__header">
  <span class="difficulty-badge difficulty-badge--beginner">Principiante</span>
  <span class="time-estimate">~60 min</span>
</div>

**Sin instalación. Sin terminal. Sin experiencia previa.** Todo corre en tu navegador a través de Google Colab. Solo necesitas una cuenta de Google.

[:material-open-in-new: Abrir el taller en Google Colab](https://colab.research.google.com/github/ClawBio/ClawBio/blob/main/docs/tutorial-variant-interpretation.ipynb){ .md-button .md-button--primary }
[:material-presentation-play: Ver las diapositivas del hackathon](https://docs.clawbio.ai/presentations/hackathon-madrid-mayo-2026/){ .md-button }
[:material-presentation-play: Ver la introducción a ClawBio](https://docs.clawbio.ai/presentations/genomica-agentica-es/){ .md-button }

!!! tip "El taller práctico del hackathon ClawBio Madrid"
    Este taller acompaña a las dos charlas del hackathon de Madrid (20 mayo 2026). Aplicarás ClawBio a un genoma humano real: anotación de variantes, farmacogenómica e interpretación clínica.

---

## Parte 1: ¿Qué es ClawBio?

### La versión corta

ClawBio es un toolkit open-source que utiliza IA para automatizar el análisis genómico. Le pasas datos genéticos, ejecuta el análisis, y obtienes un informe estructurado. No hace falta experiencia en bioinformática para empezar.

### El problema que resuelve

Interpretar el genoma de una persona implica hoy una cadena de pasos manuales: descargar software especializado, configurar bases de datos, enviar consultas a APIs web, parsear ficheros de salida en bruto y cruzar resultados entre varias fuentes. Cada paso requiere una herramienta distinta, conocimiento distinto y formatos de archivo distintos. Un solo análisis puede llevar horas o días.

A la vez, los modelos de lenguaje (como ChatGPT o Claude) responden a preguntas de genómica, pero se inventan cosas con frecuencia. Generan asociaciones gen-fármaco que no existen, citan artículos retirados y producen llamadas de alelos estrella sin base en la evidencia. En genómica clínica, los resultados alucinados son peligrosos.

ClawBio cierra esa brecha:

| Problema | Cómo lo resuelve ClawBio |
|----------|-------------------------|
| Los pipelines manuales son lentos y propensos a errores | Cada análisis se empaqueta como un "skill" de un clic con datos de demo incluidos |
| La IA alucina biología | Cada skill está anclado a bases de datos publicadas (ClinVar, CPIC, gnomAD), no a las suposiciones del modelo |
| La reproducibilidad está rota | Cada ejecución produce un paquete de reproducibilidad (comandos exactos, checksums, versiones) |
| Los datos genéticos son sensibles | Todo el procesamiento ocurre en tu máquina (o en tu sesión de Colab). No se sube nada a los servidores de ClawBio. |

### Quién lo usa

ClawBio lo utilizan estudiantes, investigadores y bioinformáticos. Es open-source (licencia MIT), gratis, y tiene una comunidad creciente:

| | |
|---|---|
| **Estrellas en GitHub** | 750+ |
| **Forks** | 85+ |
| **Skills disponibles** | 40+ (anotación de variantes, farmacogenómica, GWAS, single-cell RNA-seq, puntuación de equidad y más) |
| **Contribuidores** | 20+ |

El proyecto se lanzó en enero de 2026 y se ha utilizado en hackathons (Imperial College, DoraHacks, Madrid), cursos universitarios (Westminster, UCL) y laboratorios de investigación.

---

## Parte 2: Lo que necesitas saber antes del taller

No hace falta memorizar nada de esto antes de empezar la práctica. Léelo una vez para familiarizarte con los términos y consúltalo cuando avances por el notebook.

### ¿Qué es la variación genómica?

El ADN de cada persona difiere del "genoma de referencia" en unas 4 a 5 millones de posiciones. Estas diferencias se llaman variantes. El tipo más común es el polimorfismo de un solo nucleótido (SNP): una letra del ADN cambiada por otra (por ejemplo, A por G en una posición concreta).

La mayoría de las variantes no afectan a la salud. Una pequeña parte sí cambia cómo funcionan las proteínas, cómo se metabolizan los fármacos o si alguien tiene mayor riesgo de una enfermedad. El reto es encontrar las importantes.

### ¿Cómo se clasifican las variantes?

El American College of Medical Genetics and Genomics (ACMG) utiliza cinco categorías:

| Categoría | Qué significa | Qué ocurre clínicamente |
|-----------|--------------|------------------------|
| **Patogénica** | La variante causa o contribuye fuertemente a la enfermedad | Se informa al paciente. Se ofrece asesoramiento genético. |
| **Probablemente patogénica** | Evidencia fuerte, pero no concluyente | Se informa con la advertencia de que la evidencia aún se está acumulando. |
| **VUS** (variante de significado incierto) | No hay evidencia suficiente para decir si importa | **No se actúa.** Puede reclasificarse al disponer de más datos. |
| **Probablemente benigna** | Probablemente no afecta a la salud | Habitualmente no se informa. |
| **Benigna** | No causa enfermedad de forma definitiva | No se informa. |

!!! warning "Más de la mitad de las variantes conocidas son VUS"
    El atraso de clasificación es enorme y crece. "Aún no lo sabemos" es a menudo la respuesta más honesta en genómica. Esto vale para humanos y para la IA por igual.

### ¿Qué es el pipeline de anotación?

Cuando tienes una lista de variantes (en un fichero llamado VCF), necesitas averiguar qué hace cada una. El pipeline estándar es:

```
Tus variantes (fichero VCF)
    |
    v
VEP (Ensembl Variant Effect Predictor)
    --> ¿Qué gen se ve afectado? ¿Qué tipo de cambio? (missense, sinónima, frameshift, ...)
    |
    v
ClinVar (base de datos clínica del NCBI)
    --> ¿Se ha visto esta variante en pacientes? ¿Es patogénica?
    |
    v
gnomAD (base de datos de frecuencias poblacionales)
    --> ¿Cómo de común es la variante en más de 76.000 genomas?
    |
    v
Clasificación ACMG
    --> Combinando toda la evidencia: Patogénica / Probablemente patogénica / VUS / Probablemente benigna / Benigna
    |
    v
Informe
```

En este taller, ClawBio corre todo este pipeline por ti en un solo paso.

### ¿Qué es la farmacogenómica?

Algunas variantes genéticas cambian la forma en que el cuerpo procesa los fármacos. Este campo se llama farmacogenómica (PGx). Conocer tu perfil PGx antes de empezar una medicación puede evitar efectos adversos graves.

Ejemplos clave:

| Gen | Lo que afecta | Por qué importa |
|-----|--------------|----------------|
| **CYP2D6** | Codeína, tamoxifeno, antidepresivos (51 fármacos en total) | Los "metabolizadores pobres" no reciben analgesia de la codeína porque no la convierten en morfina |
| **CYP2C19** | Clopidogrel (anticoagulante), fármacos para la acidez | Los "metabolizadores pobres" con clopidogrel siguen con riesgo pleno de ictus o infarto porque el fármaco no se activa |
| **CYP2C9 + VKORC1** | Warfarina (anticoagulante) | Una dosis incorrecta provoca hemorragias peligrosas (demasiado) o trombos (demasiado poco). La dosis depende de los dos genes a la vez. |
| **TPMT** | Azatioprina (inmunosupresor) | Los "metabolizadores pobres" sufren supresión letal de la médula ósea a dosis estándar |
| **DPYD** | 5-fluorouracilo (quimioterapia) | La deficiencia puede ser letal a dosis estándar de quimio |

[CPIC](https://cpicpgx.org/) (Clinical Pharmacogenetics Implementation Consortium) publica guías basadas en evidencia que vinculan resultados genéticos con recomendaciones farmacológicas. Los skills de ClawBio implementan estas guías directamente.

### El problema de equidad en genómica

La mayor parte de la investigación genómica se ha hecho en personas de ascendencia europea:

- El **86%** de los participantes en estudios de asociación genómica (GWAS) son europeos
- Las bases de datos tienen **30 veces más** datos de variantes BRCA en europeos que en otras poblaciones
- Las puntuaciones de riesgo poligénico (predicciones de riesgo genético) pierden hasta el **80% de exactitud** en poblaciones no europeas

Esto significa que una variante que parece "benigna" en las bases de datos actuales puede simplemente no haberse estudiado en la población relevante. Los sistemas de IA entrenados con estos datos sesgados amplifican el problema en vez de corregirlo.

### El genoma que vamos a analizar

En este taller analizarás el genoma del Dr. Manuel Corpas, publicado en 2013 bajo licencia CC0 (dominio público). Es uno de los primeros genomas personales totalmente abiertos.

Hallazgos clínicamente relevantes reales en este genoma incluyen:

- **Factor V Leiden**: portador, riesgo aumentado de coagulación
- **HFE C282Y**: portador, hemocromatosis hereditaria (sobrecarga de hierro)
- **CFTR deltaF508**: portador, fibrosis quística
- **VKORC1 + CYP2C9**: sensibilidad a warfarina (la dosis estándar es peligrosa)
- **APOE e3/e4**: factor de riesgo elevado para enfermedad de Alzheimer

> Corpas, M. (2013). Crowdsourcing the Corpasome. *Source Code for Biology and Medicine*, **8**, 13. [doi:10.1186/1751-0473-8-13](https://doi.org/10.1186/1751-0473-8-13)

---

## Parte 3: Cómo correr el taller

### Qué necesitas

- Una **cuenta de Google** (cualquier Gmail gratuito sirve)
- Un **navegador web** (Chrome, Firefox o Safari)
- Eso es todo. Sin software a instalar, sin comandos de terminal, sin claves de API, sin pagos.

### Abrir el notebook

Pulsa el botón de abajo para abrir el notebook del taller en Google Colab:

[:material-open-in-new: Abrir en Google Colab](https://colab.research.google.com/github/ClawBio/ClawBio/blob/main/docs/tutorial-variant-interpretation.ipynb){ .md-button .md-button--primary }

Cuando se abra, verás un documento con bloques de texto y bloques de código. Los bloques de código tienen un **botón de play** a la izquierda. Pulsa el botón de play para ejecutar cada bloque en orden, de arriba abajo.

!!! tip "¿Es tu primera vez con Google Colab?"
    Google Colab es un servicio gratuito que te permite ejecutar código Python en tu navegador. No hace falta saber Python. Solo pulsa el play en cada celda de código y lee la salida. Si Colab te pide "connect to a runtime", pulsa **Connect** en la esquina superior derecha.

### Guía paso a paso

#### Paso 0: Setup (2 minutos)

Ejecuta las dos primeras celdas de código. Van a:

1. Descargar el toolkit de ClawBio (tarda unos 15 segundos)
2. Instalar las librerías de análisis necesarias

Deberías ver:

```
ClawBio loaded successfully
Skills available: 40
```

!!! tip "Si algo va mal"
    Si ves un error, pulsa **Runtime > Restart and run all** en la barra de menú de Colab. Esto reinicia todo y ejecuta las celdas desde el principio.

#### Paso 1: Explorar el genoma (5 minutos)

El notebook carga el Corpasome (el fichero de genotipado 23andMe de Manuel Corpas). Verás:

- El fichero contiene aproximadamente **600.000 SNPs**
- Cada línea tiene cuatro columnas: rsID (nombre de la variante), cromosoma, posición, genotipo
- Una tabla que muestra cuántas variantes hay en cada cromosoma (el cromosoma 1 tiene el mayor número porque es el más grande)

#### Paso 2: Seleccionar variantes clínicamente relevantes (3 minutos)

De las 600.000 variantes, el notebook extrae **21 que se sabe que son clínicamente importantes**. Incluyen variantes en genes para:

- Metabolismo de fármacos (CYP2C19, CYP2D6, CYP2C9, VKORC1, TPMT, MTHFR)
- Riesgo de cáncer (BRCA1, TP53)
- Coagulación de la sangre (Factor V, Protrombina)
- Metabolismo del hierro (HFE)
- Fibrosis quística (CFTR)
- Riesgo de Alzheimer (APOE)

El notebook las convierte a formato VCF, que es el input estándar para las herramientas de análisis genómico.

#### Paso 3: Ejecutar la anotación de variantes (5 minutos)

Éste es el análisis principal. El notebook envía las 21 variantes a la API REST de Ensembl VEP (un servicio gratuito y público del European Bioinformatics Institute) y recupera:

- En qué gen está cada variante
- Qué efecto tiene sobre la proteína (missense, sinónima, etc.)
- Si ClinVar la ha clasificado (patogénica, benigna, VUS, respuesta a fármaco)
- Cómo de común es en poblaciones mundiales (frecuencia en gnomAD)
- Un nivel de prioridad (Tier 1 = más clínicamente relevante, Tier 4 = benigna)

!!! info "No hace falta clave de API"
    La API REST de Ensembl VEP es gratuita y pública. ClawBio se encarga del formato y del envío automáticamente. Tú solo pulsas el play.

#### Paso 4: Interpretación farmacogenómica (5 minutos)

El notebook corre un segundo análisis centrado en interacciones gen-fármaco. Mapea las variantes a las recomendaciones de la guía CPIC: qué fármacos evitar, cuáles necesitan ajuste de dosis y cuáles son seguros a dosis estándar.

El hallazgo de warfarina es el resultado más llamativo (ver "Cómo interpretar tus resultados", más abajo).

#### Paso 5: Ejercicios (15 minutos, trabajo independiente)

| Ejercicio | Qué hacer | ¿Obligatorio? |
|-----------|-----------|---------------|
| **5a** | Vuelve a correr el análisis con un conjunto distinto de 20 variantes sintéticas (un clic, con la opción `--demo`). Compara los hallazgos con los del Corpasome. | Sí |
| **5b** | Si tienes tu propio fichero de 23andMe o AncestryDNA, súbelo y analiza tu propio genoma. Tus datos se quedan en la sesión de Colab y se borran al cerrar la pestaña. | Opcional |
| **5c** | Elige un gen de los resultados. Busca su función, su clasificación ACMG y su frecuencia poblacional. Escribe un párrafo breve: ¿lo informarías a un paciente? ¿Por qué sí o por qué no? | Sí |

---

## Parte 4: Cómo interpretar tus resultados

### Niveles de prioridad

ClawBio asigna a cada variante un nivel de prioridad:

| Tier | Qué significa | Ejemplo de este taller |
|------|--------------|-----------------------|
| **Tier 1** | Patogénica o probablemente patogénica. Rara (menos del 0,1% de la población). Mayor relevancia clínica. | CFTR deltaF508: portador de fibrosis quística |
| **Tier 2** | Variante de respuesta a fármaco o factor de riesgo establecido. Accionable según las guías CPIC. | VKORC1 rs9923231 TT: alta sensibilidad a warfarina |
| **Tier 3** | Variante de significado incierto (VUS). Evidencia insuficiente para clasificar. | Variantes missense raras sin entrada en ClinVar |
| **Tier 4** | Benigna o probablemente benigna. Común en la población (más del 1%). | MTHFR A1298C: polimorfismo común |

### Hallazgos clave explicados

#### Factor V Leiden (rs6025): Tier 1

**Lo que dice el resultado:** portador heterocigoto (una copia de la variante).

**Lo que significa:** el Factor V es una proteína implicada en la coagulación de la sangre. La variante Leiden hace que el sistema de coagulación sea hiperactivo, aumentando el riesgo de trombosis venosa profunda entre 3 y 8 veces.

**Por qué importa:** alrededor del 5% de la población europea es portadora. Es relevante para decisiones sobre anticonceptivos orales (que también aumentan el riesgo trombótico), planificación quirúrgica y consejos para vuelos largos. Conviene ofrecer test a familiares.

#### HFE C282Y (rs1800562): Tier 1

**Lo que dice el resultado:** portador heterocigoto.

**Lo que significa:** el gen HFE controla la absorción de hierro. Las personas con dos copias de C282Y absorben demasiado hierro, que se acumula en hígado, corazón y páncreas, provocando daño orgánico serio (hemocromatosis hereditaria). Los portadores con una sola copia tienen el hierro algo elevado, pero casi nunca desarrollan la enfermedad.

**Por qué importa:** análisis de sangre simples (ferritina sérica, saturación de transferrina) permiten monitorizar los niveles de hierro. La detección temprana en homocigotos salva vidas porque el tratamiento (donaciones regulares de sangre) es barato y eficaz.

#### CFTR deltaF508 (rs113993960): Tier 1

**Lo que dice el resultado:** portador heterocigoto.

**Lo que significa:** las mutaciones de CFTR causan fibrosis quística, una enfermedad seria que afecta a los pulmones y al sistema digestivo. Hacen falta dos copias (una de cada progenitor) para tener la enfermedad. Los portadores con una sola copia están sanos. Aproximadamente 1 de cada 25 europeos es portador.

**Por qué importa:** el estatus de portador es relevante para la planificación familiar. Si los dos miembros de una pareja son portadores de una mutación de CFTR, cada hijo tiene un 25% de probabilidad de tener fibrosis quística. Se recomienda hacer test a la pareja.

#### Sensibilidad a warfarina (CYP2C9 + VKORC1): Tier 2

**Lo que dice el resultado:** CYP2C9 *1/*2 (metabolizador intermedio) + VKORC1 rs9923231 TT (alta sensibilidad).

**Lo que significa:** la warfarina es un anticoagulante con un margen terapéutico muy estrecho. Si hay poca, se forman trombos; si hay mucha, aparecen hemorragias peligrosas. Dos genes determinan la dosis que necesita una persona:

- **CYP2C9** metaboliza la warfarina. La variante *2 ralentiza esa metabolización, así que el fármaco permanece activo más tiempo.
- **VKORC1** es la diana del fármaco. El genotipo TT hace que la diana sea más sensible, así que se necesita menos cantidad.

Esta combinación significa que el individuo del Corpasome necesita una **dosis significativamente menor a la estándar**, o bien usar un anticoagulante alternativo.

!!! danger "Éste es el ejemplo de manual de farmacogenómica salvando vidas"
    Sin test genético, un médico podría prescribir la dosis estándar de warfarina. En este individuo, esa dosis podría causar una hemorragia. El test farmacogenómico preventivo detecta esto antes de la primera prescripción.

#### APOE e3/e4 (rs429358 + rs7412): factor de riesgo

**Lo que dice el resultado:** genotipo APOE e3/e4.

**Lo que significa:** el gen APOE tiene tres formas comunes: e2, e3 y e4. La variante e4 es el factor de riesgo genético común más potente para la enfermedad de Alzheimer de inicio tardío. Una copia (e3/e4) aumenta el riesgo unas 3 veces respecto al genotipo más común (e3/e3). Dos copias (e4/e4) lo aumentan unas 12 veces.

**Contexto importante:** APOE e4 es un factor de riesgo, no un diagnóstico. Muchos portadores nunca desarrollan Alzheimer, y muchos pacientes con Alzheimer no son portadores de e4. Es un hallazgo probabilístico, no determinista. La comunicación al paciente debe acompañarse siempre de asesoramiento genético.

#### MTHFR C677T (rs1801133): Tier 2

**Lo que dice el resultado:** heterocigoto (una copia).

**Lo que significa:** MTHFR ayuda a procesar el folato (vitamina B9). La variante C677T reduce la actividad de la enzima a alrededor del 65% en heterocigotos y al 35% en homocigotos. Es extremadamente común: entre el 30 y el 40% de la población europea es portadora de al menos una copia.

**Contexto importante:** MTHFR es una de las variantes más sobreinterpretadas en la genómica de consumo. Para la gran mayoría de portadores no tiene relevancia clínica. Las homocigotas pueden beneficiarse de la suplementación con metilfolato durante el embarazo, pero los heterocigotos en general no necesitan ninguna acción.

### Cómo leer la tabla de salida

La tabla de variantes anotadas tiene una fila por variante. Esto es lo que significa cada columna:

| Columna | En lenguaje natural |
|---------|--------------------|
| `gene` | En qué gen está la variante (por ejemplo CYP2D6, CFTR) |
| `consequence` | Qué hace la variante a la proteína: `missense_variant` (cambia un aminoácido), `synonymous_variant` (sin cambio), `frameshift_variant` (rompe la proteína), etc. |
| `impact` | Severidad: HIGH (probablemente rompe la proteína), MODERATE (cambia la proteína pero puede tolerarse), LOW (improbable que importe), MODIFIER (región no codificante) |
| `clinvar_significance` | Lo que dice ClinVar: Patogénica, Probablemente patogénica, VUS, Benigna, Respuesta a fármaco |
| `gnomad_af` | Cómo de común es la variante a nivel mundial. Valores por debajo de 0,001 (0,1%) se consideran raros. |
| `priority_tier` | La evaluación global de ClawBio: Tier 1 (más importante) a Tier 4 (benigna) |

!!! warning "Lo que este análisis no puede decirte"
    Los arrays de genotipado de consumo (23andMe, AncestryDNA) testean unas 600.000 posiciones de los 3.000 millones del genoma. No detectan variantes estructurales, la mayoría de variantes raras ni cambios en número de copias. Un resultado "limpio" de un array de genotipado **no** significa que el genoma esté libre de variantes patogénicas. La secuenciación de genoma completo de calidad clínica es mucho más exhaustiva.

---

## Parte 5: Mensajes para llevarte a casa

1. **La biología no ha cambiado.** La IA acelera los pasos mecánicos (consultas a bases de datos, conversiones de formato, priorización), pero los fundamentos de interpretación de variantes, biología molecular, genética poblacional y contexto clínico siguen siendo imprescindibles. Sigues necesitando entender qué significa VUS antes de poder explicarlo a un paciente.

2. **La velocidad sí ha cambiado dramáticamente.** Un análisis que antes le llevaba días a un bioinformático (montar herramientas, lanzar VEP, parsear la salida, cruzar con ClinVar y gnomAD) ahora lleva minutos. El cuello de botella se desplaza del procesamiento de datos a la interpretación clínica y a la toma de decisiones.

3. **La farmacogenómica ya está salvando vidas.** Las interacciones gen-fármaco como warfarina/CYP2C9/VKORC1 no son medicina del futuro hipotética. Están implantadas hoy en hospitales que ofrecen test PGx preventivo. La base de evidencia y las guías clínicas existen ya.

4. **"Aún no lo sabemos" es una respuesta válida.** Más de la mitad de las variantes en ClinVar se clasifican como VUS. Comunicar la incertidumbre con honestidad, en vez de prometer más de lo que la genómica puede dar, es una de las habilidades más importantes en este campo.

5. **Las brechas de equidad son reales.** Cuando el 86% de la investigación se ha hecho en poblaciones europeas, las herramientas genómicas son inherentemente menos fiables para todos los demás. Los sistemas de IA entrenados con datos sesgados amplifican el problema. Cada análisis debería reconocer qué poblaciones representan los datos de referencia.

6. **Los datos abiertos hacen posible la ciencia abierta.** Todo este taller, un genoma real, herramientas open-source, APIs gratuitas y un notebook gratuito, es reproducible por cualquier persona del mundo. Esa transparencia es el estándar al que apuntar.

!!! danger "Aviso médico"
    ClawBio es una herramienta de investigación y educación. No es un dispositivo médico y no proporciona diagnósticos clínicos. Los hallazgos discutidos en este taller son únicamente con fines educativos. Consulta a un profesional sanitario antes de tomar cualquier decisión médica basada en datos genéticos.

---

## Enlaces y referencias

### Recursos del taller

| Recurso | Enlace |
|---------|--------|
| Notebook de Google Colab | [:material-open-in-new: Abrir en Colab](https://colab.research.google.com/github/ClawBio/ClawBio/blob/main/docs/tutorial-variant-interpretation.ipynb) |
| Repositorio de ClawBio en GitHub | [github.com/ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) |
| Documentación de ClawBio | [docs.clawbio.ai](https://docs.clawbio.ai) |
| Comunidad de ClawBio en Discord | [discord.gg/EEp4Neaz](https://discord.gg/EEp4Neaz) |
| Grupo de WhatsApp ES | [chat.whatsapp.com/FInuUxJa00G7Ql3T28kW4I](https://chat.whatsapp.com/FInuUxJa00G7Ql3T28kW4I) |

### Bases de datos utilizadas en este taller

| Base de datos | Qué hace | Enlace |
|---------------|----------|--------|
| Ensembl VEP | Predice el efecto funcional de las variantes | [ensembl.org/vep](https://www.ensembl.org/info/docs/tools/vep/index.html) |
| ClinVar | Asociaciones curadas entre variantes y enfermedades | [ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar/) |
| gnomAD | Frecuencias alélicas poblacionales (más de 76.000 genomas) | [gnomad.broadinstitute.org](https://gnomad.broadinstitute.org/) |
| CPIC | Guías clínicas de farmacogenómica | [cpicpgx.org](https://cpicpgx.org/) |

### Artículos clave

- Richards et al. (2015). Standards and guidelines for the interpretation of sequence variants. *Genetics in Medicine*, 17(5), 405-424. [doi:10.1038/gim.2015.30](https://doi.org/10.1038/gim.2015.30)
- Corpas, M. (2013). Crowdsourcing the Corpasome. *Source Code for Biology and Medicine*, 8, 13. [doi:10.1186/1751-0473-8-13](https://doi.org/10.1186/1751-0473-8-13)

---

## Qué viene después

Este taller ha analizado un **solo genoma** con un **array de SNP** (~600.000 posiciones). Si quieres seguir trabajando con ClawBio tras el hackathon, abre un issue o un pull request en el [repositorio de GitHub](https://github.com/ClawBio/ClawBio) o pasa por el [grupo de WhatsApp](https://chat.whatsapp.com/FInuUxJa00G7Ql3T28kW4I) y el [Discord](https://discord.gg/EEp4Neaz).
