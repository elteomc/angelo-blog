# Workshop site maintenance

## Build and preview

Run `python3 tools/build_workshop.py` once if generated includes are missing. Normal builds run that generator automatically.

Run `quarto render --output-dir /tmp/angelo-workshop-site`, then serve that directory locally. The ordinary `quarto render` command still targets docs, but nothing deploys automatically from these commands.

The current series preview is http://127.0.0.1:8878/. It serves an external render from /tmp/angelo-scale-geometry-review. Refresh the output directory to update the running preview.

## Shared layout

layouts/workshop.html owns document structure, navigation, title presentation, article contents and footer. assets/workshop/workshop.css owns the Workshop presentation. theme.js progressively adds Light, Dark and System selection. All reading content, links and expandable answers work without client-side routing.

The template marks its own title containers with quarto-title-block so Quarto does not move the heading during canonicalization. The post-render checker restores a standard HTML doctype because the installed Quarto version drops it during processing.

## Content

- Edit article prose and math in blog/*/index.qmd. These files are authoritative.
- Edit project prose in projects/*/index.qmd. The magnetic-PE page demonstrates the case-study layout classes.
- content/catalog.json defines ordered collections, their hub metadata, chapter membership, planned chapters, and project-index entries. Index titles and descriptions come from article front matter. Project summaries are catalog fields.
- _includes contains generated index fragments. Keep them available in checkouts because Quarto discovers includes before running pre-render scripts. The generator refreshes them on each build.
- The homepage introduction and selected-work arrangement are in index.qmd.
- Studio and the comparison router remain isolated in design-preview. Production pages do not depend on them.

## Adding an article

Create blog/<slug>/index.qmd with title, description, date, and ordinary Markdown content. Folder metadata provides the author, Writing navigation and relative asset prefix. For a series chapter, set series-label, previous-url/title and next-url/title, and add its source to the catalog. Each collection has groups entries controlling group labels and chapter ranges. Set series-url to the root-relative hub path so article navigation reaches the right collection.

Standalone articles can use the same article template without series metadata. Add their source paths to the articles list in content/catalog.json to include them in the writing index. Collections are listed separately in the Writing index. A chapter without a source uses its catalog title and description, displays Planned on the hub, and never receives a link or an archive entry. Set review-notice on a written draft to display its review status.

For another project, add its source and a catalog entry with title, url, topic, date, description, image and alt text. The generator checks that its source exists. Use custom-layout only when the page supplies its own full layout and h1.

## Checks

The build fails for broken local links, missing assets, missing fragment targets, duplicate IDs or an incorrect h1 count. Browser checks cover actual math rendering, theme persistence, native answer expansion and responsive layout.

Visible figure captions and article subtitles are hidden through presentation rules, not removed from their sources. Internal experiment reports are not linked or bundled as reader resources. No source experiment data has been deleted.

For the scale and geometry figures, run python3 tools/scale_geometry_figures.py. Verify numerical examples with python3 tools/check_scale_geometry.py and collection behavior with python3 tools/test_series_catalog.py.

For parts 3 and 4, run python3 tools/check_decay_momentum.py to verify the finite-step examples and trajectory identities. Run python3 tools/decay_momentum_figures.py to rebuild their three figures. Render review-only work outside docs.

For parts 5 and 6, run python3 tools/check_layer_duality.py to verify the activation and support examples. Run python3 tools/layer_duality_figures.py to rebuild their two diagrams. Keep review builds outside docs.


For Parts 7 through 12, run `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_series_completion.py`. Rebuild the six figures with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/angelo-blog-matplotlib python3 tools/series_completion_figures.py`. These commands use NumPy and Matplotlib in the existing environment.

The finite frozen-teacher control uses eight equally weighted inputs in four dimensions and 45 target norm ratios. It directly evaluates analytically specified representatives, with no optimizer training. Reproduce its saved record with `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_series_completion.py --results specs/006-complete-scale-geometry-series/frozen-teacher-results.json`. The record stays in the source repository and is not bundled as a reader resource.

Scale and geometry chapters have ordered source entries in the catalog. Chapter footer links display P: or N: followed by the respective title. The first chapter has only N:, and the last has only P:. The shared layout preserves descriptive previous and next assistive labels.


For the practical follow-up drafts, run `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_practical_followups.py`. Use `--tables` to inspect the numerical values printed in the polar and averaging articles. Rebuild all four figures with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/angelo-blog-matplotlib python3 tools/practical_followup_figures.py`.

Parts 13 through 15 were approved for publication November 5, 2026. Future review builds should stay outside docs until approval. Article review notices identify local drafts. The series hub keeps its simple presentation and uses a fourth chapter group. Part labels have no fixed total, and the established title-based P: and N: links connect the sequence.


For Parts 16 through 18, run python3 tools/check_network_scaling.py. Rebuild the residual, width-transfer, and normalized-head figures with python3 tools/network_scaling_figures.py. Render the local review outside docs. Parts 16 through 18 were reviewed and approved for publication November 5, 2026. Future review batches stay outside docs until approval.


For Parts 19 through 21, run python3 tools/check_geometry_evidence.py. Rebuild their three figures with python3 tools/geometry_evidence_figures.py. The internal experiment-record.json contains selected source-hashed aggregates from the existing study, rather than a new training result. Keep review output outside docs and review at http://127.0.0.1:8878/blog/scale-geometry-19/index.html.


Parts 19 through 21 were reviewed and approved for publication November 5, 2026. Future batches stay in external review output until approval.


For Parts 22 through 24, run python3 tools/check_noise_sharpness_symmetry.py. Rebuild the three figures with python3 tools/noise_sharpness_symmetry_figures.py. The valley comparison evaluates an explicit smooth three-dimensional loss for 3000 updates, without running neural-network training. Review at http://127.0.0.1:8878/blog/scale-geometry-22/index.html and keep output outside docs until approval.


Parts 22 through 24 were reviewed and approved for publication November 5, 2026. Future batches remain in external review output until approval.


For Parts 25 through 27, run `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_stochastic_feature_response.py`. Rebuild the three figures with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/angelo-blog-matplotlib python3 tools/stochastic_feature_response_figures.py`. The selected experiment record retains source hashes and archived aggregates, without a new training run. Keep review builds outside docs and review at http://127.0.0.1:8878/blog/scale-geometry-25/index.html.


Parts 25 through 27 were reviewed and approved for publication November 5, 2026. Future batches remain in external review output until approval.


For Parts 28 through 30, run `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_stability_central_flows.py`. Rebuild the three figures with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/angelo-blog-matplotlib python3 tools/stability_central_flow_figures.py`. The example record evaluates an explicit two-variable polynomial for 400 updates, without neural-network training. Review at http://127.0.0.1:8878/blog/scale-geometry-28/index.html and keep output outside docs until approval.


Parts 28 through 30 were reviewed and approved for publication November 5, 2026. Future batches remain in external review output until approval.


For Parts 31 through 33, run `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_width_feature_operators.py`. Rebuild the three figures with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/angelo-blog-matplotlib python3 tools/width_feature_operator_figures.py`. The internal example record contains exact finite linear and moment calculations and one-step centered tanh evaluations. Review at http://127.0.0.1:8878/blog/scale-geometry-31/index.html and keep output outside docs until approval.


Parts 31 through 33 were reviewed and approved for publication November 5, 2026. The approved release refreshes their pages in the verified external build before validating and installing the whole site.
