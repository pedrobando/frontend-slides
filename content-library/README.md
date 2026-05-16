# Content Library

Reference material for building presentations. Each folder contains the source content (converted from DOCX to Markdown) for a presentation series.

## Structure

```
content-library/
├── README.md                          ← this file
├── lead-conversion-os/
│   ├── vol-01-lead-conversion-os.md   ← Modules 00-10 + Appendices (Sessions 1-5)
│   └── appendix-c-pipeline-stages-tags.md ← Pipeline Stages & Tags (Session 6)
└── [future-series]/
    └── ...
```

## How to Use

1. **Before building a new session**, read the relevant content library file to understand the full source material.
2. **Reference specific modules** by section headers (e.g., `## Module 02 — The 5-Pillar Frame`).
3. **Scripts are bilingual** — every script has EN and ES versions ready to use.
4. **Tables and data** are formatted for easy extraction into slide content.
5. **When creating a new series**, convert the source DOCX files to markdown and add them here before building any slides.

## Adding New Content

When Pedro provides new DOCX files for a presentation series:
1. Create a new folder: `content-library/[series-name]/`
2. Convert each DOCX to a clean markdown file with all content preserved.
3. Include: series name, source filename, which sessions it covers, and a table of contents at the top.
4. Preserve all scripts (EN + ES), tables, rules, and appendices verbatim.
