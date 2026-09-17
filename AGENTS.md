# MLFE Lab website maintenance

The user is the sole editor and requests updates conversationally. Preserve factual content and author order. Do not infer status, dates, roles or English transliteration.

## Architecture
- Standard-library Python generator: scripts/build.py.
- Data: content/site.json, content/people/*.json, content/news/*.json, content/publications.json, content/pages/*.json, content/contact.json.
- Styles, scripts, original images: assets/.
- Public generated files: docs/. Do not edit generated HTML directly.
- No deployment workflow is configured. Confirm the destination repository and publication scope first.
- Internal links must stay relative to support repository subpaths.

## Updating
- Keep person ids stable; news and publications reference ids.
- Alumni: set group to Alumni and provide graduated/placement only when known. Preserve activity records.
- News date/end_date use ISO dates; date controls ordering.
- Specify publication members. These papers render globally and on associated current profiles.
- Imported member activities preserve source differences. Review matching entries when changing paper titles/status.
- Never crop research equation images.
- Preserve Google Sites until the user requests transition.
- Never rerun migration helpers over edited content. migration/ is a local historical archive.

## Verify
Run python scripts/build.py and python scripts/validate.py.
For layout changes, check desktop/mobile, image loading and menu behavior.
Never overwrite unrelated research repositories.


## Language policy
Use English for the public site. The Home “Our research” introduction is the only bilingual prose section. Preserve Korean alumni names until verified English names are supplied; never invent romanizations. Original photographs/documents remain unchanged. The user requested the Submitted list without research-area subcategories.
