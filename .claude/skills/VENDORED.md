# Skills in this folder

| Skill | Origin | License |
|---|---|---|
| `spacetime-physics` | Written for this project | MIT (project license) |
| `astropy` | KalarisLabs/research-agent-skills, `skills/astropy` | MIT (see `KALARIS-LICENSE`) |
| `uncertainty-and-units` | KalarisLabs/research-agent-skills, `skills/uncertainty-and-units` | MIT (see `KALARIS-LICENSE`) |
| `citation-verification` | KalarisLabs/research-agent-skills, `skills/citation-verification` | MIT (see `KALARIS-LICENSE`) |

The three KalarisLabs skills were copied unchanged from
https://github.com/KalarisLabs/research-agent-skills at commit
`e2c8aa0fba85f4f3e42c8cc329ec06c443d9af24` (2026-11-13). They were reviewed before copying.
The only network access is in `citation-verification/scripts/verify_citations.py`, which
queries api.crossref.org, api.openalex.org and export.arxiv.org. Do not set
`CROSSREF_MAILTO` to the owner's personal email without asking.

To update one, re-copy that skill's folder from a newer commit, review the diff, and update
the commit hash above.
