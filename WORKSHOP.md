# Workshop site maintenance

## Build and preview

Run `python3 tools/build_workshop.py` once if generated includes are missing. Normal builds run that generator automatically.

Run `quarto render --output-dir /tmp/angelo-workshop-site`, then serve that directory locally. The ordinary `quarto render` command still targets docs, but nothing deploys automatically from these commands.

The current review server is http://127.0.0.1:8877/ and the comparison preview remains at http://127.0.0.1:8876/.

## Shared layout

layouts/workshop.html owns document structure, navigation, title presentation, article contents and footer. assets/workshop/workshop.css owns the Workshop presentation. theme.js progressively adds Light, Dark and System selection. All reading content, links and expandable answers work without client-side routing.

The template marks its own title containers with quarto-title-block so Quarto does not move the heading during canonicalization. The post-render checker restores a standard HTML doctype because the installed Quarto version drops it during processing.

## Content

- Edit article prose and math in blog/*/index.qmd. These files are authoritative.
- Edit project prose in projects/*/index.qmd. The magnetic-PE page demonstrates the case-study layout classes.
- content/catalog.json defines the ordered series membership and project-index entries. Index titles and descriptions come from article front matter. Project summaries are catalog fields.
- _includes contains generated index fragments. Keep them available in checkouts because Quarto discovers includes before running pre-render scripts. The generator refreshes them on each build.
- The homepage introduction and selected-work arrangement are in index.qmd.
- Studio and the comparison router remain isolated in design-preview. Production pages do not depend on them.

## Adding an article

Create blog/<slug>/index.qmd with title, description, date, and ordinary Markdown content. Folder metadata provides the author, Writing navigation and relative asset prefix. For a series chapter, set series-label, previous-url/title and next-url/title, and add its source to the catalog. The series_groups entries in the catalog control group labels and chapter ranges.

Standalone articles can use the same article template without series metadata. Add their source paths to the articles list in content/catalog.json to include them in the writing index. This release has one six-part series, not a general publishing CMS.

For another project, add its source and a catalog entry with title, url, topic, date, description, image and alt text. The generator checks that its source exists. Use custom-layout only when the page supplies its own full layout and h1.

## Checks

The build fails for broken local links, missing assets, missing fragment targets, duplicate IDs or an incorrect h1 count. Browser checks cover actual math rendering, theme persistence, native answer expansion and responsive layout.

Visible figure captions and article subtitles are hidden through presentation rules, not removed from their sources. Internal experiment reports are not linked or bundled as reader resources. No source experiment data has been deleted.
