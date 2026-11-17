# Guion del video — FlowForge DE (4 minutos 20 segundos)

Título recomendado: **FlowForge DE | Automated Data Engineering with dbt, DuckDB & GitHub Actions (No AWS)**

**00:00–00:25 — Presentación / mostrar la portada y el repositorio**

“Hola, en este video presentaré FlowForge DE, un proyecto open source de ingeniería de datos que construí utilizando Python, dbt, DuckDB y GitHub Actions. Su propósito es automatizar todo el proceso que convierte archivos de origen en un dashboard público, sin usar AWS.”

**00:25–00:55 — Arquitectura / mostrar el diagrama 02**

“En primer lugar, Python genera registros sintéticos de pedidos, clientes y productos. Estos se cargan en DuckDB; luego dbt organiza transformaciones SQL en capas de staging, hechos y marts. Finalmente exportamos un archivo JSON agregado para un dashboard alojado en GitHub Pages.”

**00:55–01:35 — Fuente de datos / mostrar el código Python en GitHub**

“El generador crea 3.200 pedidos, 260 clientes y 48 productos de forma reproducible. Los pedidos contienen estados como completado, cancelado o reembolsado. Una validación importante consiste en excluir las ventas no completadas de los ingresos. Por eso mantenemos separadas la ingesta y la transformación.”

**01:35–02:18 — dbt / mostrar `models/staging/stg_orders.sql` y `models/marts/fct_completed_orders.sql`**

“Los modelos dbt estandarizan tipos y nombres. Después relacionamos los pedidos con sus productos y clientes, calculamos ingresos y beneficios, y agregamos resultados mensuales por región y categoría. Además, las pruebas de dbt revisan claves únicas, campos obligatorios y relaciones entre tablas.”

**02:18–02:55 — Automatización / mostrar `.github/workflows/pipeline.yml` y Actions**

“GitHub Actions orquesta las etapas: instala dependencias, genera datos, ejecuta pruebas Python, ingesta datos a DuckDB, corre `dbt build`, exporta y valida el JSON. La ejecución se activa con commits, manualmente o mediante una programación diaria. Si una prueba falla, no se publica una versión defectuosa.”

**02:55–03:38 — Dashboard / mostrar la web pública**

“Este es el dashboard de FlowForge. Permite filtrar por año y región y observar ingresos, número de pedidos, beneficios, margen, tendencias y distribuciones. El sitio es estático y recibe solo información agregada. Los datos mostrados son sintéticos para fines educativos.”

**03:38–04:20 — Cierre / mostrar el repositorio y Medium**

“Como resultado tenemos un proceso completo, reproducible y automatizado, publicado con servicios gratuitos. En la descripción incluyo el repositorio con el código, las pruebas, la automatización y el artículo técnico en Medium. Gracias.”

**Nota:** si no hay CI exitoso o sitio público, no digas que están completados: muestra el código de configuración y explícalo como pendiente. No uses diagramas para fingir capturas de una ejecución real.
