# Skill Architecture

This project contains three Codex skills with deliberately separate responsibilities.

## 1. `scientific-infographic`

Type: scientific information design skill.

Primary function:

- Transform complex scientific content into a structured academic infographic.
- Prioritize information architecture, module hierarchy, and reader comprehension.
- Select appropriate layouts such as columns, comparison, flow, timeline, matrix, multi-panel, or map-like structure.

Typical inputs:

- Topic or title.
- Research field.
- Content type.
- Core information points.
- Research object.
- Language.
- Aspect ratio.
- Text density.
- Color system.
- Forbidden elements.

Workflow:

1. Extract the scientific topic and communication goal.
2. Classify the content type.
3. Select a layout strategy.
4. Choose an academic palette.
5. Build a structured image-generation prompt.
6. Run quality checks for clarity, hierarchy, density, and credibility.
7. Call ChatGPT image generation unless the user requests prompt-only output.

Quality standard:

- The reader should understand the topic and module structure at a glance.
- Every graphic element should support explanation.
- The result should feel like a high-quality review figure or academic teaching diagram, not a PPT template.

## 2. `scientific-cover-visual`

Type: scientific concept-art and editorial cover skill.

Primary function:

- Convert a research theme into a memorable scientific cover visual.
- Prioritize concept, focal image, visual tension, and editorial polish.
- Avoid copying real journal covers, logos, or institutional identities.

Typical inputs:

- Cover theme or title.
- Research field.
- Research object.
- Core mechanism or visual concept.
- Key visual elements.
- Cover type.
- Language.
- Aspect ratio.
- Text requirement.
- Palette and composition preference.
- Forbidden elements.

Workflow:

1. Distill the theme into a short visual concept.
2. Select a cover composition strategy.
3. Decide whether text, fictional journal naming, or pure visual output is appropriate.
4. Choose a palette with stronger editorial impact than a paper figure.
5. Generate the prompt.
6. Check for originality, brand safety, and non-template composition.
7. Call ChatGPT image generation unless prompt-only output is requested.

Quality standard:

- The image should have one strong focal concept.
- The scientific object or mechanism should be recognizable.
- The visual should feel like a research cover, not a commercial ad, beauty ad, or generic technology poster.

## 3. `scientific-paper-figure`

Type: scientific mechanism and publication figure skill.

Primary function:

- Generate publication-grade scientific figures with clear mechanism, anatomy, sequence, or workflow.
- Prioritize causal path, structural correctness, and concise labels.
- Support graphical abstracts, mechanism diagrams, anatomy diagrams, surgery figures, pathology mechanisms, and experimental workflows.

Typical inputs:

- Figure type.
- Research topic.
- Research field.
- Research object.
- Core mechanism.
- Input.
- Process.
- Output.
- Key visual elements.
- Structure format.
- Language.
- Aspect ratio.
- Text requirement.
- Palette.
- Forbidden elements.

Workflow:

1. Extract the research object and mechanism.
2. Decompose the content into input, process, and output.
3. Select the scientific narrative structure.
4. Determine where magnified insets, arrows, labels, and panels are needed.
5. Generate a mechanism-focused prompt.
6. Check scientific credibility and path clarity.
7. Call ChatGPT image generation unless prompt-only output is requested.

Quality standard:

- The figure must answer what the object is, what starts the process, what happens in the middle, and what result is produced.
- Arrows and labels must serve the mechanism.
- Visual polish must not override scientific plausibility.

## Shared Design Boundary

All three skills avoid:

- Real journal logos.
- Real institutional branding.
- Unverified medical claims.
- Decorative visual noise.
- Overcrowded labels.
- Generic PPT style.
- Cheap blue-purple technology backgrounds.
- Text-heavy layouts that image models cannot render reliably.

