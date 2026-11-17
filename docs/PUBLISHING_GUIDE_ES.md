# Guía de entrega — FlowForge DE

Repositorio: https://github.com/Gino019/automated-data-engineering-project

## 1. Publicar en GitHub

El conector GitHub de este chat permite lectura pero denegó escritura HTTP 403. Por eso se entrega un ZIP con `.git` y commits ya preparados. Extrae el ZIP, abre PowerShell dentro de la carpeta y ejecuta:

```powershell
git remote -v
git branch -M main
git push -u origin main
```

El `origin` ya está configurado en el ZIP. Si GitHub te pide iniciar sesión, autentícate en tu cuenta Gino019. Si el repo cambió, ejecuta `git fetch origin` y revisa las diferencias antes de hacer push. No uses `--force`.

## 2. Activar GitHub Pages

1. Visita https://github.com/Gino019/automated-data-engineering-project/settings/pages
2. En Build and deployment, Source: GitHub Actions.
3. Visita https://github.com/Gino019/automated-data-engineering-project/actions
4. Selecciona "FlowForge DE — ELT, Tests & Pages". Si fuera necesario, pulsa "Run workflow".
5. Comprueba que tanto `pipeline` como `deploy` terminen con marca verde. Si alguno falla, revisa los logs.
6. Abre https://gino019.github.io/automated-data-engineering-project/

### Cómo comprobar que el dashboard es resultado real de dbt

En la sección Execution metadata debe aparecer `dbt-duckdb automated ELT pipeline` y un identificador de GitHub Actions, no `synthetic preview` ni `PREVIEW ONLY`. Esta distinción importa: el preview local es una demostración sin dbt, mientras que el resultado de CI debe provenir de la pipeline completa.

## 3. Medium: imagen por sección

| Archivo | Dónde colocarlo | Tipo |
|---|---|---|
| `01-cover.png` | Después del título | Ilustración de portada |
| `02-architecture.png` | Sección 1 / arquitectura | Diagrama real del diseño |
| `03-dbt-lineage.png` | Sección 5 | Diagrama conceptual de modelos |
| `06-data-quality.png` | Sección 6 | Ilustración de validaciones |
| `04-dashboard-preview.png` | Sección 7 | Captura de la previsualización sintética |
| `05-ci-workflow-illustration.png` | Sección 8 | Diagrama ilustrativo, NO ejecución GitHub real |

Abre https://medium.com/new-story. Pega `docs/MEDIUM_ARTICLE_EN.md`, coloca las imágenes con Insert image de Medium y preserva los bloques de código. Antes de publicar, cambia `[Add your name]` por tu nombre, elimina los marcadores `[FIGURE ...]` y verifica que los enlaces de GitHub y Pages funcionan.

**Evidencia académica recomendada:** agrega adicionalmente una captura auténtica de GitHub Actions donde los dos jobs están verdes y una captura auténtica de la aplicación desplegada, una vez que las hayas comprobado. No uses ilustraciones para fingir ejecuciones.

## 4. Video de máximo 5 minutos

Lee `docs/VIDEO_SCRIPT_ES.md`. Graba pantalla (OBS Studio, Xbox Game Bar o cualquier grabador) mostrando repositorio, modelos SQL, workflow GitHub Actions, dashboard y Medium. Duración propuesta: 4:20. Publica el video como público o no listado accesible, según tu consigna.

## 5. Entrega por ZIP

Completa las URL reales en `submission/links_template.txt` (la plantilla tiene marcadores). Luego ejecuta:

```bash
python scripts/make_submission.py
```

Obtendrás `FlowForge_DE_submission_links.zip` con los enlaces del repositorio, la aplicación, Medium, video y workflow.

**IMPORTANTE:** No afirmes haber publicado Medium o YouTube hasta hacerlo manualmente. Debes enviar los enlaces reales al grupo indicado por el docente cuando corresponda.
