# Angelo's research website: design and development plan

Status: approved by Angelo for staged implementation on 2026-10-18. Each substantial batch requires review before an explicitly approved commit.

Date: 2026-10-18

## 1. Purpose and intended impression

Build a personal research website that makes Angelo's intellectual interests, explanatory ability, and actual work immediately tangible. The site should feel carefully made, visually curious, technically confident, and welcoming to a potential collaborator.

The desired impression is: this person understands things deeply, makes ideas accessible, builds interesting things, and would be enjoyable to think with.

Three experiences must coexist:

1. A visitor can quickly understand who Angelo is and identify a few substantial things to explore.
2. A reader can settle into a precise explanation, with pictures and interaction helping at the right moments.
3. A returning reader can follow new work without every update needing the production effort of a major publication.

The design should support the commitment to publish at least twice weekly. Its default authoring path must remain simple. Special visual treatment should be available where it materially strengthens a piece.

This document proposes the direction, architecture, reusable formats, implementation sequence, and review process. It does not authorize publication, commits, domain changes, or replacing the existing site.

## 2. What is agreed and what remains proposed

### Agreed preferences

- Draw from several references while developing a recognizable identity of our own.
- Borrow Zahavy's publications structure specifically. His homepage is not the desired visual model.
- Borrow Karpathy's clarity of communication, sequencing, and prioritization of material.
- Explore the visual presence and interaction that Angelo likes in Shakir Mohamed's site.
- Preserve the human character of Olah's illustrations while pursuing the production quality of Distill.
- Treat Ciechanowski's reader-controlled explanations as a major interaction reference.
- Consider short embedded Manim animations. Long-form video production is not an immediate goal.
- Give unfinished thinking a legitimate but quieter home.
- Distinguish formal publications from essays, paper notes, and projects.
- Give substantial publications their own shareable presentation, potentially with a separate domain or subdomain.
- Develop reusable layouts and allow sections to have different moods.
- Review significant choices together. Explain the rationale and tradeoffs before asking for a decision.
- Preserve the previously proposed priority order: homepage, writing index, article opening, project page, figure system, then selective interaction.

### Proposed defaults, not settled decisions

- Retain Quarto as the publishing foundation.
- Use a warm editorial base with more expressive figures and project surfaces.
- Begin the notebook as a distinct area of the same site, with a single discreet entry point.
- Give publication pages stable paths first. Add separate hostnames when a particular work benefits from one.
- Keep a shared typography and navigation system across different page types.
- Prototype two visual directions before selecting one.
- Use a compact publications archive with optional filters and independently designed publication pages.

These defaults can be revised during review. They are not substitutes for Angelo's aesthetic judgment.

## 3. Baseline and existing work

The current site is a Quarto website with rendered output in `docs/`. It has light and dark themes, mathematical typesetting, code presentation, a writing listing, a six-part free-probability draft series, and a series landing page.

Relevant sources include:

- `_quarto.yml`: site structure, navigation, rendering, resources, and themes.
- `index.qmd`, `blog.qmd`, `projects.qmd`, `notes.qmd`, `about.qmd`, and `cv.qmd`.
- `styles.css`, `theme-light.scss`, `theme-dark.scss`, and `math-layout.css`.
- `free-probability.qmd` and `blog/free-prob-*/index.qmd`.
- `assets/free-probability/` and `tools/free_probability_figures.py`.
- `EDITORIAL_PLAN.md`: the publishing commitment and a proposed series release queue.

The existing series is draft material for joint content review. Design work must not imply that its claims, voice, or release readiness have been approved. The dates in the editorial plan are proposals, not an active publishing schedule.

The repository contains substantial existing uncommitted work, including staged files. Future implementation must preserve that state, record which changes belong to the redesign, and avoid blanket staging, resets, or replacement of unrelated files.

### Design observations

The reading body has a useful foundation: restrained color, serif prose, clear mathematical notation, and room around figures. The main weakness is that broad styling makes unlike pages feel too similar.

The homepage has an article-like table of contents. The writing list repeats metadata and shrinks explanatory diagrams into tiny previews. Article openings contain several competing descriptive layers. Projects and the series hub lack a strong visual identity.

These are reasons to develop page-specific composition within the existing system. They do not establish a need for a framework migration.

## 4. Reference synthesis

The following are design interpretations from the comparative review, refined by Angelo's feedback. Borrow principles and behaviors, not assets, wording, or entire page compositions.

| Reference | Specific lesson | Translation to this site |
| --- | --- | --- |
| [Zahavy publications](https://www.tomzahavy.com/publications) | Compact bibliography, author and venue hierarchy, domain and method filters | A structured publications archive with clear routes to paper, code, and local explanation |
| [Karpathy](https://karpathy.ai/) | Prioritized sections and direct explanations of what each item offers | Separate selected work from recency and give every featured item a clear reason to open it |
| [Shakir Mohamed](https://shakirm.com/) | Personal visual presence and a more expressive presentation | Explore composed imagery and restrained movement, then choose the particular effects together |
| [Olah](https://colah.github.io/) | Conceptual pictures with personality | Explanatory sketches, memorable visual metaphors, and topic collections |
| [Distill](https://distill.pub/) | Carefully produced explanatory figures | Shared visual conventions, readable annotations, and generous space for complex diagrams |
| [Transformer Circuits](https://transformer-circuits.pub/) | Different emphasis for major publications and small updates | Several publishing formats with clear levels of prominence |
| [Ciechanowski](https://ciechanow.ski/) | Direct manipulation embedded in explanation | Small experiments where changing a parameter exposes a relationship |
| [World Models](https://worldmodels.github.io/) | A publication has its own explorable home | Dedicated research pages with paper, code, results, and demonstrations |
| [Matuschak](https://andymatuschak.org/) | Ongoing thinking can be a serious public practice | A connected notebook with a quieter position in the site's hierarchy |
| [Breitner](https://www.joachim-breitner.de/) | Personal interests coexist with technical work | An About page with specific human details, avoiding a generic professional biography |
| [Weng](https://lilianweng.github.io/) | Consistent long-form learning notes | Low-friction writing templates, without adopting the entire visual style |

Zahavy's current archive states that it is ordered by citation count. Borrowing its organization does not commit us to that ranking. A selected section followed by reverse chronology is a better initial proposal for this site. Filters should become visible when the actual collection makes them useful.

The World Models reference concerns the independent identity of a publication. Its spacing, title proportions, and mathematical typography are not the target.

## 5. Audience journeys

### A potential collaborator

Arrives at Home, understands the research interests, opens a selected project, sees the main result and Angelo's role, then finds code and contact information. This should require no guesswork about whether a piece is a tutorial, original research, or an exploratory project.

### A reader arriving at one article

Understands the question and prerequisites, encounters a concrete example early, and can follow a diagram without losing their place. Related material and the next chapter are available after the explanation.

### Someone evaluating a publication

Finds the title, authors, venue or status, central contribution, paper, and code immediately. Can read a visual overview, inspect results and limitations, and obtain citation information.

### A returning reader

Sees what is new without confusing it with the portfolio's selected work. Can follow a series in order and subscribe to the main writing feed.

### Someone interested in unfinished thought

Enters through one Notebook link, sees clearly dated working material, and can return to the main site. Notebook pages remain discoverable within that area without taking over the homepage or ordinary writing feed.

## 6. Information architecture

Proposed top-level navigation:

**Angelo Farfan → Home | Writing | Projects | Publications | About**

The name is the Home link, so an additional Home label may be unnecessary. CV and contact belong in About and the footer. Notebook should have one quieter entry, likely in the footer or a secondary navigation position. Exact placement is a review decision.

Avoid exposing empty sections merely to suggest a larger body of work. A publications layout can be prepared before it deserves a permanent top-level link. The inventory of real material determines which sections launch.

### Separate content type from topic

Content types describe the reader's experience: essay, tutorial, paper note, project, publication, notebook entry, and series hub.

Topics describe subject matter: free probability, learning theory, formal reasoning, algorithms, and other areas supported by actual work. Do not create a large speculative taxonomy.

A piece has one primary content type and a small number of topic labels. A project can link to several posts and a publication without duplicating all their text.

### Selected work and latest work

Home is curated. Writing is primarily chronological, with selected entry points and series collections. Publications are bibliographic. Projects are organized around artifacts and questions.

A six-part series receives one substantial featured entry on Home. Individual chapters remain accessible through the series hub and archive. The normal archive must not accidentally present chapter two as the beginning of the learning path simply because of equal dates or default sorting.

## 7. Visual direction and identity

### Proposed identity

A personal research studio with an editorial reading experience: warm, precise, a little playful, and visibly made by someone who cares about explanation.

Recognizable identity should come from repeated choices:

- A consistent approach to diagrams and annotation.
- Deliberate title and section proportions.
- A small palette with stable semantic roles.
- Real project imagery.
- Distinctive but controlled motion.
- Specific personal language and visible intellectual curiosity.

### Two directions to prototype

| Direction | Appearance | Strength | Risk |
| --- | --- | --- | --- |
| A: Editorial workshop | Warm paper, ink-like text, restrained accent, human annotations, precise diagrams | Strong combination of mathematical seriousness and personality | Can become too quiet if featured work lacks visual weight |
| B: Experimental studio | More contrast, bolder compositions, larger project imagery, selective animated surfaces | Stronger immediate presence and sense of active experimentation | Can become distracting or expensive to maintain |

Both prototypes should use identical real content. Produce the homepage and the same article opening in each direction so we compare visual choices rather than different writing quality.

A likely synthesis is A for sustained reading and some of B for featured projects. That remains a hypothesis to judge visually.

### Typography

Use one deliberate prose family and one complementary interface family. Verify the fonts actually load, and use metric-compatible fallbacks where practical. Keep mathematical notation visually compatible with the prose.

Starting values for prototypes, not fixed requirements:

- Prose around 18 to 20 CSS pixels on desktop, adjusted for the selected font.
- Reading measure around 60 to 72 characters.
- Line height around 1.55 to 1.75.
- Titles scaled by page purpose and viewport, not one oversized global rule.
- Small metadata that stays readable rather than fading into the background.

Test long titles, dense formulas, subscripts, inline code, and captions before selecting the type system.

### Section moods

Home and Projects may be more expressive. Articles remain calm. Publications feel precise and authoritative. Notebook feels compact and workmanlike while retaining the same level of care.

Share the masthead, spacing vocabulary, typography families, focus states, and basic controls. Variation should come from composition, imagery, accent usage, and content density.

## 8. Page and component specifications

### Home

Composition:

1. Name and a concise, specific introduction.
2. A meaningful visual anchor, either a portrait, a figure from the work, or a small authored illustration.
3. Two or three selected works with an image, title, one-sentence promise, and clear destination.
4. Selected writing or a currently featured series.
5. A smaller recent-writing list.
6. A brief current-interest or personal line, if Angelo wants one.
7. Contact and quiet secondary links.

Remove the homepage table of contents. Avoid a screen-height decorative introduction that hides the work. The visual anchor must also work as a still image.

### Writing archive

Use compact rows for ordinary entries and a more generous treatment for selected essays or series. Each row needs a title, short description, date, and optional content-type label. Repeated author names are unnecessary on a single-author archive.

Create deliberate preview images. A thumbnail should show a recognizable concept, not an entire scientific plot with illegible labels. Text-only entries should look intentional.

Add topic filtering when it helps a real collection. Keep reset and empty states obvious. Ordinary browsing must still work without client-side filtering.

### Essay and tutorial

Opening: small topic or series label, title, one useful summary, compact date and reading information, then the question or concrete example.

Body: narrow prose, optional wider figures, consistent captions, optional margin notes, readable mathematics, code where useful, and quiet navigation. Use a table of contents only when the length benefits from it.

Ending: conclusions at the appropriate level of certainty, sources, related work, and the next chapter if relevant. Distinguish intuition, derivation, numerical evidence, and an open question through clear language and occasional reusable blocks.

### Paper note

A lighter article format with a source card, the question addressed, central idea, assumptions, Angelo's interpretation, and unresolved questions. Avoid a large header or a mandatory custom illustration.

A polished paper note belongs in Writing. Raw reading fragments belong in Notebook. The distinction is editorial completeness, not length alone.

### Project case study

Opening: title, concise problem statement, prominent result image or demo, role, collaborators if applicable, status, and code or demo links.

Body: motivation, approach, the consequential design choices, evidence, limitations, and what changed in Angelo's understanding. Include a reproducible entry point where one exists.

The AGOP work is a candidate pilot, not an automatically selected project. Inspect the actual project artifacts before promising a result, illustration, or performance claim.

### Publications archive

Use compact bibliographic rows inspired by Zahavy. Each record supports title, ordered authors, year, venue or preprint status, domain, method, and paper, code, presentation, and local-page links.

Subtly identify Angelo in the author list. Distinguish accepted work, preprints, and other outputs accurately. Do not populate this archive with paper summaries presented as Angelo's publications.

Proposed order: selected publications, then the complete list by year. Domain and method filters appear only when there is enough variety to justify them. If introduced, show result count, active filters, and a clear reset. Citation-count sorting is deferred unless explicitly wanted.

### Dedicated publication page

A stable shareable destination with a lighter site header and the work's own visual accent. Include title, authors, affiliations where appropriate, status or venue, a concise contribution statement, paper and code links, an overview figure, results, limitations, and citation information.

A publication page may contain a full explanation or link to a separate accessible essay. Keep the paper, overview, and tutorial distinct when their audiences differ.

### Series hub

Short promise, prerequisites, and a numbered visual path through the chapters. Each chapter has one question and a clear place in the sequence. Use fixed ordering and consistent previous/next navigation.

For free probability, prototype six chapter entries with small conceptual diagrams rather than six full plots. Keep publication status clear. A chapter should not be labeled released merely because its draft exists locally.

### About and CV

Use a concise research biography, education and experience supported by existing records, a few specific personal interests, contact, and the actual CV when available. Avoid empty destination pages and generic self-promotion.

## 9. A quiet home for unfinished thinking

The notebook should be one deliberate step away from the portfolio. It should not be hidden behind misleading navigation or require readers to understand a complex knowledge graph.

| Option | Benefits | Costs |
| --- | --- | --- |
| Same-site `/notebook/` area | Shared publishing setup, simple links, easy promotion of a note | Separation is mostly editorial and visual |
| `notes.<verified-site-domain>` | Stronger sense of entering a different workspace | Extra hosting, search, navigation, and deployment decisions |
| Separate registered domain | Maximum independence | More maintenance and a weaker immediate relationship to the main site |

Recommendation: prototype the same-site area first, while leaving the structure portable to a subdomain. The current configured domain is not evidence of DNS control or hosting readiness.

Notebook behavior:

- One discreet entry point from the main site and an obvious return link.
- Short status labels such as working note or open question, plus an updated date.
- Separate listing and feed from polished writing.
- Explicit choice about whether main-site search includes it. Proposed default: separate scope with an option to include notebook results.
- Contextual links to polished work where useful.
- A promotion path from working note to edited article, preserving the relationship between versions.

Quiet visibility does not provide privacy. Only material intentionally prepared for public access belongs here. Search-engine indexing is a decision to make before release, not an assumption attached to the folder name.

## 10. Publication URLs and domains

Every substantial publication should have a dedicated URL regardless of whether it has a separate domain.

Proposed initial structure: a stable path such as `/research/<slug>/`, with a self-contained presentation and explicit links back to the portfolio. These are proposed routes, not existing pages.

For a major collaborative work, a dedicated domain or subdomain can be worthwhile. Before choosing one, agree on ownership, who maintains it, hosting, canonical URL, and what happens when the work is updated.

If the same work appears at more than one address, designate one canonical page and use redirects where supported. Preserve paper links and existing incoming URLs. Do not create multiple competing copies of the same publication just to obtain several domains.

## 11. Diagrams, animation, and interaction

### Three media modes

| Mode | Best use | Proposed implementation |
| --- | --- | --- |
| Static illustration | A relationship that can be understood at a glance | SVG for suitable diagrams, optimized raster images for other material |
| Short authored animation | A sequence, transformation, or derivation | Rendered Manim clip or a small native animation with playback controls |
| Reader-controlled experiment | A question involving changing parameters or comparing states | Browser-native SVG or Canvas with accessible HTML controls |

Manim can produce short rendered animations for embedding. Embedding a video does not make its mathematical scene respond to arbitrary reader input. Ciechanowski-style manipulation requires a separate interactive implementation or a deliberately constrained precomputed system. We should choose the medium from the teaching goal.

Initial animation proposal: short, silent, captioned clips around 5 to 20 seconds, with play, pause, and replay. This is a prototype range, not a requirement for every post. Avoid uncontrolled looping beside dense prose. Respect reduced-motion preferences and provide a useful poster frame.

### Figure language

- Shared colors for repeated mathematical roles within a series.
- Explicit labels and line styles so color is not the only distinction.
- Consistent line weights, text sizes, arrows, and caption conventions.
- Human annotations where they explain a decision or intuition.
- Separate export sizes for article figures and archive previews.
- Light and dark presentation checked deliberately. A contained light figure panel is acceptable where recoloring would damage meaning.
- Source and reuse permission recorded for external assets.

### Pilot interaction candidates

1. Eigenbasis rotation: change a two-dimensional relative angle and observe how the spectrum of a sum changes. Clearly label this as finite-dimensional geometry, not a demonstration of asymptotic freeness.
2. Crossing versus noncrossing pairings: select a pairing and see its geometric structure, alongside the relevant combinatorial explanation.
3. Empirical versus predicted spectra: compare precomputed experiment outputs under a small set of parameters, with model assumptions and finite-size limitations visible.

Start with one pilot. Choose it after the article design is approved. Do not build a general simulation platform before knowing whether the small interaction improves the explanation.

Every interactive figure needs a clear prompt, a meaningful initial state, labeled controls, reset behavior, keyboard and touch access, and an explanation that remains useful if the interaction fails to load.

## 12. Sustainable authoring and content records

Ordinary publishing should use a template and existing components. An author should not have to edit global styles or build a new JavaScript component to publish a paper note.

Proposed shared fields: title, slug, content type, summary, date, updated date, topics, status, selected flag, and optional preview image with alternative text.

Additional fields by type:

- Series: series identifier, chapter order, prerequisites.
- Project: role, collaborators, repository, demo, related articles.
- Publication: authors, venue, year, paper URL, code URL, citation, domain and method categories.
- Notebook: working status and related polished work.

Use one source of truth for publication metadata so the archive and dedicated page do not drift. Define draft, review-ready, and released states before building new listings. Validate how those states affect rendering, feeds, and search rather than assuming a label alone hides a page.

For the twice-weekly cadence, vary production effort. A concise edited note and a larger explanation can coexist. Custom motion is an enhancement, not a prerequisite for meeting the commitment.

## 13. Technical approach

Retain Quarto initially. Its documented article layouts and listings support much of the proposed structure. Use scoped page classes and reusable components rather than adding more global selectors that affect unrelated pages.

Likely implementation areas:

| Area | Expected changes |
| --- | --- |
| Navigation and rendering | `_quarto.yml`, explicit inclusion and exclusion of new content types |
| Design foundations | Theme files and shared tokens for color, typography, spacing, and motion |
| Page composition | Homepage, archive, project, publication, and notebook layouts |
| Article components | Figure wrappers, compact metadata, series navigation, source cards |
| Metadata | Small structured records for publications and shared content fields |
| Media | Versioned source assets and optimized web exports |
| Discovery | Search scopes, series order, feeds, metadata, and stable URLs |

The current render pattern explicitly covers root pages and `blog/*/index.qmd`. New research or notebook directories will need intentional inclusion. Planning documents should remain excluded from public output.

Use client-side interaction only where it adds value. Text, navigation, citations, and static figures should remain usable without custom scripts. Prefer precomputed numerical data for expensive demonstrations. Avoid adding a server solely for visual polish.

Preserve existing URLs wherever possible. If a route changes, prepare a migration map and verify redirects on the actual hosting platform. Confirm that platform before prescribing deployment configuration.

## 14. Delivery phases and review gates

Each phase ends with a small, concrete result to review. Do not ask Angelo to judge every spacing value or inspect an entire redesign at once.

| Phase | Deliverable | Review question | Exit condition |
| --- | --- | --- | --- |
| 0: Inventory | Real content and asset list, URL map, baseline screenshots, repository change boundary | Which work should represent you first? | Pilot content selected without inventing claims |
| 1: Visual directions | Two homepage concepts and matching article openings using identical content | Which feels like you, and what feels generic or excessive? | Direction and desired expressive level selected |
| 2: Homepage and writing | Responsive homepage, compact archive, selected-work treatment | Does this present the right priorities immediately? | Clear hierarchy and approved personal presence |
| 3: Article and series | One complete article and the six-part hub using reusable components | Is it comfortable to read, and do the visuals improve understanding? | Long-form layout approved before rolling across all drafts |
| 4: Project and publications | One real project page, compact publication archive prototype, one publication-page layout | Are contribution, evidence, and destinations obvious? | Clear separation of projects, publications, and tutorials |
| 5: Media pilot | One short animation or interactive figure with static fallback | Does manipulating or watching this teach something useful? | Learning purpose demonstrated without excessive overhead |
| 6: Notebook | Quiet entry point and one representative working note | Is the separation sufficient and the status clear? | Visibility, search scope, and hosting choice agreed |
| 7: Consolidation | Real-content migration, authoring instructions, final verification | Is this ready to become the public site? | Content and design reviewed, release separately authorized |

The figure system begins in Phase 1 and matures through the article and project work. It should not be postponed until the end. Publication templates can use clearly marked local fixtures if no appropriate public record is ready. Fixtures must never appear as real achievements in the deployed site.

A useful first milestone is Phases 0 through 3: the public face and reading experience become coherent before we add more specialized surfaces. Further work can proceed incrementally without blocking ordinary writing.

## 15. Verification and acceptance

### Visual and editorial

- Review Home, archive, article, project, publication, and notebook examples at phone, tablet, and desktop widths.
- Check the selected light and dark treatments with real figures and mathematical notation.
- Ensure long titles and missing optional images remain well composed.
- Make the first article screen communicate the subject and opening idea rather than mostly metadata.
- Make project results and primary links visible early.
- Keep notebook entries out of curated portfolio surfaces by default.
- Confirm that descriptions, role claims, publication status, and citations reflect actual work.

### Interaction and accessibility

- Keyboard access, visible focus, semantic headings, labeled controls, and sufficient contrast.
- Touch controls that do not depend on hover or precise dragging alone.
- Reduced-motion behavior and controllable playback.
- No page-wide horizontal overflow. Wide mathematics can scroll within its own region.
- Static alternatives for interactive figures and meaningful image descriptions.
- Main reading content remains available when optional media or scripts fail.

### Performance and maintainability

Proposed engineering budgets to validate during prototyping: ordinary pages should avoid downloading video before user intent, prevent media-driven layout shifts, and load only the scripts needed by their page type. Aim for no more than roughly 1 MB of initial transferred assets on ordinary text pages, with explicit exceptions reviewed for media-heavy work.

Measure representative pages on a throttled mobile profile. Use measured results to refine budgets. A technically elaborate hero is not acceptable if it delays access to the work.

Add an article and a project through the authoring path as a maintainability check. Verify links, search scope, feeds, publication filters, chapter ordering, and draft exclusion. Use focused tests for these behaviors, not tests that merely restate CSS choices.

### Release boundary

Verify generated output separately from source changes. Inspect the exact release diff, preserve unrelated work, and review the site in a private preview. Commit and deploy are separate actions requiring Angelo's explicit instruction in this collaboration. Domain purchases and DNS changes also require a concrete reviewed proposal.

Update `FUNCTIONALITIES.md` when implementation adds capabilities. Record actual discovered code issues in `ISSUE_REGISTRY.md`. This planning document itself adds no website capability.

## 16. Decisions to discuss at the right time

Do not turn this into a long questionnaire before any visual evidence exists.

| Decision | When to ask | What to show |
| --- | --- | --- |
| Editorial warmth versus stronger experimental presentation | Before implementation of the visual system | Two comparable homepage and article concepts |
| Portrait, project visual, or authored illustration | Homepage review | The same composition with meaningful alternatives |
| Which Shakir-style effects resonate | Visual-direction review | Specific examples of transitions, imagery, and movement |
| Which project represents Angelo first | Inventory | A short list grounded in actual artifacts |
| Notebook name and entry placement | Notebook prototype | Main-site navigation beside the notebook entrance |
| Same-site notebook versus subdomain | Before hosting work | Concrete maintenance and discovery consequences |
| Publication sort order and filters | Archive prototype | Real records where possible, clear fixtures otherwise |
| Dedicated domain for a particular publication | When a real work needs it | Proposed URL, ownership, canonical link, and deployment plan |
| Animation versus direct manipulation | Media pilot | A storyboard and the question the figure teaches |
| Final readiness | Before release | The complete preview and exact changes |

Ask one or two related questions at a time. Explain the recommended choice, what it gains, and what it costs. A general enthusiasm for the direction should not be treated as approval of every future aesthetic or infrastructure decision.

## 17. Risks and scope controls

| Risk | Response |
| --- | --- |
| A collage of borrowed aesthetics | Use one type system, shared diagram conventions, and repeated compositional rules |
| Endless redesign displacing study | Ship the smallest reviewed milestone and preserve the twice-weekly authoring path |
| Every post becomes a production | Keep paper notes and ordinary articles complete without custom media |
| Polished visuals imply stronger evidence than exists | Label numerical experiments, intuition, original results, and working hypotheses accurately |
| Notebook overwhelms the portfolio | Separate discovery surfaces and use one discreet entry point |
| Domain proliferation | Start with stable paths and add hostnames for a clear purpose |
| Global styling breaks specialized layouts | Scope styles by component and page type |
| Preview accidentally includes drafts or fixtures | Verify release selection and generated output explicitly |
| Existing work is overwritten | Record the baseline and keep redesign changes narrowly attributable |
| Personal voice disappears in templates | Review real prose and images with Angelo before broad rollout |

Deferred unless later justified: a framework migration, accounts, a comment system, a custom content management system, citation-count synchronization, a large knowledge graph, long-form video production, and a general-purpose interactive mathematics engine.

## 18. Definition of success

A new visitor can identify Angelo's interests and open meaningful work quickly. A reader encounters explanations whose typography, figures, and interaction feel deliberately composed. A collaborator can distinguish original contributions from learning notes and find the relevant code or paper. Unfinished thought has a clear home without dominating the public introduction.

Most importantly, publishing twice a week remains realistic because the design does the repetitive work. Major pieces can receive more expressive treatment while the entire site still feels like one person's thoughtful body of work.

The immediate next step after discussing this plan is the paired visual-direction prototype. No full-site redesign should begin before that comparison.

## 19. Technical reference notes

- [Quarto article layout](https://quarto.org/docs/authoring/article-layout.html): supported body, wider-page, and margin content arrangements.
- [Quarto document listings](https://quarto.org/docs/websites/website-listings.html): configurable listing formats and content metadata.
- [Quarto interactivity](https://quarto.org/docs/interactive/): available approaches for interactive documents.
- [Quarto video embedding](https://quarto.org/docs/authoring/videos.html): embedding video within authored pages.
- [Manim Community documentation](https://docs.manim.community/en/stable/): mathematical animation authoring and rendering.

These support feasibility. Specific library choices, browser behavior, hosting settings, and rendering costs must be verified when implementing the selected prototype.

## 20. Approval and prototype batch 01

Angelo approved the proposed identity and the paired visual-direction comparison. Implementation starts with isolated homepage and article-opening prototypes. Commit only after presenting each substantial batch and receiving explicit approval.

The video-led presentation at [How might we learn?](https://andymatuschak.org/hmwl/) is a future reference: opening video, right-hand contents, and supporting snapshots. Defer this layout until appropriate original video material exists.

Batch 01 is in `design-preview/`. It does not replace the existing Quarto pages. The review toolbar switches Workshop and Studio while retaining the current page.

## 21. Prototype progress after feedback

Revision 02 removed decorative diagrams and promotional captions, retained the spacious layout, and differentiated an editorial homepage from a profile-and-work index. Neither direction is selected as final.

Revision 03 extends both directions through a writing index, series overview, and complete draft reading layouts. Existing chapter content is imported for visual evaluation, not newly approved for release. Video-led layouts, new project case studies, publication pages, and the notebook remain later work. Each substantial batch still requires review before any commit.

## Project presentation and separator preference

Revision 04 implements the approved magnetic-PE case study in the isolated preview. Use whitespace or separate lines for metadata, without middle-dot separators. The project layout introduces experiment context, a full-width result figure, paired uncertainty, a narrative with local navigation, and source records. Everything remains uncommitted for review.

## Editorial preferences after revision 05

Show figures without visible captions. Keep useful alternative text. Do not expose internal experiment records or report downloads. Use the compact project facts for context. Write from the author’s perspective with concrete decisions, questions and observations, allowing personality without invented anecdotes or inflated claims.

## Heading and hierarchy refinement

Revision 06 favors specific research or mathematical headings over generic scaffolding. Remove redundant uppercase accent labels when spacing and heading type already convey the hierarchy. Result summaries should align with the figure’s panel layout rather than resemble standalone dashboard statistics.

## Approved homepage and discovery batch

Workshop is the selected primary direction, with Studio retained for comparison. Revision 09 refines selected work on the homepage, creates a real project index and polishes navigation on desktop and mobile. The batch is ready for review and remains uncommitted.

## Workshop core implementation

The approved direction now runs natively through Quarto using shared templates, catalog-generated indexes and ordinary page URLs. Studio remains a comparison snapshot. The migration has passed local build, math, link and responsive checks and is awaiting review without committing.
