#!/usr/bin/env python3
"""Nuxt file inventory, adapted from master-templates/scripts/sync-catalogs.template.py.

Uses bounded filesystem scopes and the catalog Markdown templates. This is not
a TypeScript AST parser: verify exported symbols and model semantics in source.
Run with Python 3.10+ from any working directory.
"""

from datetime import datetime, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SUFFIXES = {'.ts', '.js', '.mts', '.mjs', '.vue', '.sql', '.prisma'}
EXCLUDED = {'node_modules', '.nuxt', '.output', '.git'}
SERVICE_SCOPES = (
    'app/composables', 'app/services', 'app/utils',
    'server/api', 'server/routes', 'server/utils', 'shared/utils',
)
MODEL_SCOPES = (
    'app/models', 'app/types', 'server/models', 'server/database',
    'shared/models', 'shared/types', 'prisma', 'drizzle', 'database',
)


def inventory(scopes):
    """Return existing candidate files; do not infer classes or schema relations."""
    paths = set()
    for scope in scopes:
        directory = ROOT / scope
        if directory.is_dir():
            for path in directory.rglob('*'):
                if (path.is_file() and path.suffix in SUFFIXES
                        and not EXCLUDED.intersection(path.relative_to(ROOT).parts)):
                    paths.add(path.relative_to(ROOT).as_posix())
    return sorted(paths)


def render(template_name, marker, body):
    source = (ROOT / '.agents/master-templates/memory' / template_name).read_text(encoding='utf-8')
    source = re.sub(r'^<!-- TEMPLATE_VERSION:.*?-->\s*', '', source)
    source = re.sub(r'\{\{#' + marker + r'\}\}.*?\{\{/' + marker + r'\}\}',
                    lambda _: body, source, flags=re.S)
    source = source.replace('{{ISO_TIMESTAMP}}', datetime.now(timezone.utc).isoformat(timespec='seconds'))
    source = source.replace('{{PRIMARY_KEY_STRATEGY}}', 'Not configured; inspect future models before choosing a strategy')
    source = source.replace('{{COMPRESSED_LOOKUP_MODELS_LIST}}', 'No catalog of lookup models is inferred by this file scanner')
    source = source.replace('- *All lookup models use standard Not configured; inspect future models before choosing a strategy primary keys and key-value naming.*', '')
    if '{{' in source:
        raise ValueError(f'Uncompiled catalog placeholder in {template_name}')
    return source.strip() + '\n'


def rows(paths):
    return '\n'.join(f'| [{path}](../../../{path}) | Source candidate; verify symbols and behavior before reuse. |' for path in paths)


def main():
    services = inventory(SERVICE_SCOPES)
    models = inventory(MODEL_SCOPES)
    catalog_dir = ROOT / '.agents/memory/catalogs'
    catalog_dir.mkdir(parents=True, exist_ok=True)
    surfaces = [p for p in ('app/app.vue', 'nuxt.config.ts', 'index.html', 'compose.yml') if (ROOT / p).is_file()]
    service_body = ('## Bounded Nuxt source inventory\n\n'
                    'Scopes: ' + ', '.join(f'`{scope}/`' for scope in SERVICE_SCOPES) + '.\n\n'
                    'This inventories files, not exported functions, factories, or application classes.\n\n')
    service_body += ('| Candidate | Evidence |\n| --- | --- |\n' + rows(services)
                     if services else 'No source candidates found in the listed service/helper scopes.\n')
    service_body += '\n\n## Existing application and deployment surfaces\n\n| File | Evidence |\n| --- | --- |\n' + rows(surfaces)
    model_body = ('## Bounded data inventory\n\n'
                  'Scopes: ' + ', '.join(f'`{scope}/`' for scope in MODEL_SCOPES) + '.\n\n'
                  'Type files are candidates, not proof of database models. The scanner does not infer tables, keys, migrations, or relationships.\n\n')
    model_body += ('| Candidate | Evidence |\n| --- | --- |\n' + rows(models)
                   if models else 'No model, type, schema, or migration candidates found in the listed scopes.\n')
    (catalog_dir / 'services.md').write_text(
        render('services.template.md', 'DISCOVERED_SERVICES_BY_DOMAIN', service_body), encoding='utf-8', newline='\n')
    (catalog_dir / 'models-schema.md').write_text(
        render('models-schema.template.md', 'DISCOVERED_MODEL_CLUSTERS', model_body), encoding='utf-8', newline='\n')
    print(f'Catalog inventory refreshed: {len(services)} service/helper files; {len(models)} data candidates. Semantic review required.')


if __name__ == '__main__':
    main()
