# Workflow

This repository is designed around a simple production workflow:

```text
User request
  ↓
Choose the correct skill type
  ↓
Extract structured inputs
  ↓
Select visual strategy
  ↓
Build generation prompt
  ↓
Run quality gate
  ↓
Generate image with ChatGPT
  ↓
Review and iterate if needed
```

## Step 1: Choose the Skill

Use `scientific-infographic` when the goal is clarity.

Use `scientific-cover-visual` when the goal is impact.

Use `scientific-paper-figure` when the goal is mechanism accuracy.

## Step 2: Extract Inputs

The agent should extract the necessary fields from the user request. Missing non-critical fields can be inferred. For medical, anatomical, surgical, or pathology content, ask a minimal follow-up question if the missing information would likely create a wrong figure.

## Step 3: Select Visual Strategy

Each skill chooses its own visual strategy:

- Infographic: columns, comparison, timeline, matrix, panels, map-like structure.
- Cover: strong subject, micro-universe, concept metaphor, structural cutaway, dynamic process, minimalist cover.
- Paper figure: input-process-output, A-B-C-D sequence, main body plus magnified inset, micro-to-macro, anatomy cutaway.

## Step 4: Build Prompt

Prompts should be structured and production-oriented:

- Role.
- Task.
- Input fields.
- Layout or composition.
- Palette.
- Scientific constraints.
- Forbidden elements.
- Final quality standard.

## Step 5: Generate Image

Default behavior:

- If the user asks for an image, call ChatGPT image generation.
- If the user asks for prompt-only output, return the prompt.

## Step 6: Review

Review against the skill-specific quality gate:

- Infographic: information hierarchy and readability.
- Cover: concept strength and originality.
- Paper figure: mechanism path and structural credibility.

When the first result fails a gate, iterate with one focused correction rather than rewriting the entire prompt.

## Multi-skill Case Workflow

For complex biomedical topics, use the three skills as a small production pipeline instead of forcing all goals into one image.

Example: mechanisms of anesthesia drugs.

```text
1. scientific-cover-visual
   -> create the high-impact concept image.

2. scientific-infographic
   -> map the whole topic into teaching or review modules.

3. scientific-paper-figure
   -> split each causal mechanism into a publication-style figure.
```

This keeps SOLID-style responsibility boundaries at the workflow level:

- Cover visuals optimize for impact.
- Infographics optimize for explanation.
- Paper figures optimize for causal and structural accuracy.
