# Guion del taller, Hackathon ClawBio Madrid

Versión para el slot de 12:30 a 13:00 (briefing e introducción). Tiempos por diapositiva entre paréntesis. No leerlo: usarlo como guía y soltar los puentes en vivo. Total aproximado, 22 minutos.

---

**Slide 1 · Título (30 s)**
Buenas tardes a todos. Gracias por venir, gracias a Nebrija por la sede, y gracias en especial a los que habéis cogido un vuelo o un AVE para estar hoy aquí. Soy Manuel Corpas, vengo de la University of Westminster, en Londres. En los próximos veinte minutos quiero contaros tres cosas: qué es la genómica agéntica, por qué existe ClawBio, y qué vais a construir esta tarde.

**Slide 2 · Nueva frontera (1 min)**
La biología se ha convertido en una ciencia saturada de datos. Un solo genoma humano son tres mil millones de pares de bases. Interpretarlo en clínica significa alinear lecturas, llamar variantes, anotarlas, cruzarlas con la literatura, y al final escribir un informe que un médico pueda leer en cinco minutos. Cada paso depende de una herramienta distinta, con sus dependencias y su configuración. Por eso aparecieron Nextflow, Snakemake o Galaxy. Aun así, si eres biólogo y quieres analizar tus propios datos, tienes tres opciones: aprender a programar, contratar a alguien, o conformarte con una interfaz que casi nunca hace lo que necesitas.

**Slide 3 · Arnés (1 min)**
Los modelos ya son lo bastante buenos. Pueden escribir código, depurarlo, ejecutarlo, planificar varios pasos. Pero si le dices a un LLM genérico "anótame este VCF", la salida varía entre sesiones, se inventa asociaciones gen-fármaco, y a veces clasifica variantes patogénicas que no existen. El problema no es el modelo. El problema es el arnés: qué herramientas puede invocar, qué barreras evitan errores silenciosos. La ingeniería agéntica es la disciplina de construir ese arnés.

**Slide 4 · IA agéntica (1 min)**
Hace tres o cuatro años, los LLM en biología servían para resumir artículos. Útil, pero incremental. Una IA que te contaba cosas. Lo que está pasando ahora es cualitativamente distinto. Cuando conectas un LLM a un sistema de archivos, a una base de datos, a tu terminal, se convierte en un agente que planifica, ejecuta, ve qué falla y se adapta. El papel del investigador cambia: dejas de construir el análisis y pasas a evaluarlo.

**Slide 5 · Qué es un agente (1.5 min)**
Ésta es la definición que usamos en un Perspective reciente con Segun Fatumo y Heinner Guio. Cuatro condiciones necesarias. Una: autonomía, decisiones en tiempo de ejecución. Dos: restricción al dominio, no código desde cero, sino una biblioteca de skills validados. Tres: refinamiento iterativo, si algo falla, lo diagnostica e intenta arreglarlo. Cuatro: mediación en lenguaje natural, no hace falta saber programar. Si quitas cualquiera de las cuatro, no tienes un agente, tienes otra cosa.

**Slide 6 · Comparativa (1 min)**
El cuello de botella se mueve. En un flujo tradicional, el cuello de botella es producir código. En un flujo agéntico, ese coste se evapora, pero aparece otro: el cuello de botella de validación. Tienes que mirar lo que el agente ha hecho y decirle "esto está mal, repítelo". La capacidad de juzgar se vuelve la habilidad escasa.

**Slide 7 · Tabla (1 min)**
En workflows de exoma y de single cell, el tiempo de puesta en marcha pasa de horas a quince minutos. La supervisión deja de ser continua. La reproducibilidad sube porque el skill está versionado. Ojo a la última fila: el modo principal de fallo deja de ser "te has equivocado de versión de samtools" y pasa a ser "el resultado parece bueno pero no lo es". Los errores ya no se ven, hay que buscarlos.

**Slide 8 · Sección genómica (10 s)**
Vale. Vamos a la genómica.

**Slide 9 · Qué es ClawBio (1.5 min)**
ClawBio es un toolkit open source de skills para agentes de IA en bioinformática. Cada skill es un contrato, un archivo SKILL.md que encapsula código, datos de referencia, inputs, outputs y tests. La IA lo lee y lo ejecuta, pero no puede sobrescribirlo. De ahí sale el determinismo. Hoy: más de cuarenta skills, setecientas cincuenta estrellas en GitHub, doscientas plazas aquí en Madrid, y cero coste. Licencia MIT.

**Slide 10 · Tracks (2 min)**
Aquí entráis vosotros. Tres tracks. Primero: un nuevo skill. Anotación de variantes, rutas, informes clínicos, farmacogenómica, o lo que se os ocurra. A las cuatro y media nos lo enseñáis. Segundo: encadenar varios skills para resolver una pregunta de varios pasos. Tomáis una muestra, la procesáis, la anotáis, generáis el informe, lo demostráis en vivo. Tercero: equidad. HEIM es un framework que hemos desarrollado para puntuar representación ancestral en datasets, y vais a auditar datasets reales para encontrar dónde hay sesgo. No hace falta experiencia previa en bioinformática: si sabéis programar pero no de biología os ponemos con un biólogo, y al revés.

**Slide 11 · Limitaciones (1.5 min)**
Antes de lanzaros, una advertencia. La IA agéntica baja la barrera para generar análisis, no para juzgarlos. Cuatro fallos que tenéis que tener en la cabeza. Uno: errores silenciosos plausibles. Tuvimos un skill que devolvió "farmacogenómica normal" para un fichero vacío, nadie se dio cuenta hasta que un revisor lo pilló. Dos: alucinación, asociaciones gen-enfermedad inventadas. Tres: sesgo de equidad, el ochenta y seis por ciento de los datos GWAS son europeos, si dejas que el agente decida por defecto automatizas el sesgo a escala. Cuatro: la brecha de validación. Un usuario que empieza no ve los errores que sí ve un analista con diez años de experiencia. La democratización es real, pero parcial.

**Slide 12 · Democratización (45 s)**
Dicho eso, la barrera de infraestructura ya no existe. No necesitas cluster, ni acuerdos de acceso a datos, ni equipo de bioinformática. Todo corre en vuestro portátil o en Colab. Las estadísticas resumen son públicas. ClawBio es MIT. Un investigador en Lima, en Kampala o en Madrid corre los mismos análisis que uno en el Broad Institute.

**Slide 13 · Sur Global (1 min)**
Esto enlaza con trabajo abierto con Segun Fatumo en Queen Mary y con la red LatinOMICS. Tres ejes: infraestructura, que sustituimos por Colab; datos, estadísticas resumen públicas; formación, lo que estamos haciendo hoy. Si os interesa este tema, mañana y pasado, aquí mismo, la sesión LatinOMICS dos del Congreso incluye la Declaración de Medellín.

**Slide 14 · Sección manos a la obra (10 s)**
Vale, manos a la obra.

**Slide 15 · Programa (1.5 min)**
Este es el plan de las próximas seis horas. Ahora, briefing. A la una formáis equipos y arranca el hackathon. Tres, pausa café. Tres y cuarto, seguimos. Cuatro y media: demos, cinco minutos por equipo. Cinco y media: premios y networking. Seis: cerramos. Tres premios: mejor nuevo skill, mejor flujo agéntico, mejor hack de equidad. Detalles a las cuatro y media, pero ya os adelanto que los jurados son externos.

**Slide 16 · Cómo empezar (1.5 min)**
Lo que tenéis que hacer en los próximos diez minutos. Tres enlaces, abrid cada uno en una pestaña nueva. Uno: la presentación técnica de ClawBio en castellano, está en docs.clawbio.ai/presentations/genomica-agentica-es. Es la charla larga sobre genómica agéntica, validación y el benchmark de farmacogenómica, por si queréis profundizar después. Dos: el taller práctico, también en castellano, en docs.clawbio.ai/tutorials/variant-interpretation-workshop-es. Está pensado para correrlo en Google Colab, sin instalación, anotando un genoma humano real. Y tres: el repositorio en github.com/ClawBio/ClawBio. El install script en macOS y Linux tarda menos de cinco minutos. Y antes de que se me olvide: entrad al grupo de WhatsApp. Es el canal por defecto para dudas y para compartir los enlaces a vuestros repos.

**Slide 17 · Take-home (1.5 min)**
Cinco mensajes que os lleváis a casa. Uno: la IA acelera lo mecánico, pero la experiencia del dominio no se atajan. Dos: la farmacogenómica está salvando vidas hoy, warfarina con CYP2C9 y VKORC1 está en hospitales ya. Tres: "aún no lo sabemos" es una respuesta válida; más de la mitad de las variantes son de significado incierto, y eso es honestidad. Cuatro: el análisis transancestral no es opcional, comprobad siempre si lo que encontráis se transfiere. Cinco: la infraestructura ya no es la barrera. Vuestro portátil más Colab dan análisis de calidad publicable, gratis, en cualquier sitio.

**Slide 18 · Comunidad (45 s)**
Aunque hoy se acabe el evento, ClawBio sigue. WhatsApp para el grupo activo, Discord donde está RoboTerri (nuestro agente conversacional), GitHub para issues y contribuciones. Si lo que hacéis hoy os gusta, ése es el sitio para seguir.

**Slide 19 · Mañana, congreso (1 min)**
Un anuncio antes de daros la palabra: si ya estáis en Madrid, mañana y pasado, en este mismo edificio, está el Tercer Congreso Español de Medicina Genómica. Carracedo abre con la estrategia nacional, Alfonso Valencia del BSC habla del Espacio Europeo de Datos Sanitarios, Khalid Fakhro viene de Sidra Medicine en Qatar, Carmen Ayuso, Lapunzina, Iacoangeli desde King's, Silvia Alvarez desde Regeneron. Noventa y cinco euros presencial, sesenta online. Inscripción en congresogenomica.com.

**Slide 20 · Recursos (30 s)**
Aquí tenéis todos los enlaces. Esta presentación, la charla técnica completa en castellano, el taller práctico con Colab, el repositorio, los datos del Corpasome en Zenodo, el grupo de WhatsApp, y la inscripción al congreso de mañana. Todo en castellano. Y con eso, ¿preguntas rápidas o nos lanzamos a formar equipos?
