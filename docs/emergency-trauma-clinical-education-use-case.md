# Use Case: Emergency Trauma Clinical Education

This use case shows how the three skills can support emergency trauma teaching materials without turning the output into clinical guidance.

The intended input is a de-identified educational outline, checklist, or Markdown knowledge-base page. The intended output is a set of visual teaching aids: a cover visual, a structured infographic, and one or more workflow or mechanism figures.

## Safety Boundary

All outputs in this use case are for educational visualization only. They are not clinical guidance, triage rules, treatment protocols, or patient-specific advice.

Do not include:

- Identifiable patient information.
- Real hospital, emergency department, trauma center, ambulance, or institution names.
- Real clinician names, patient initials, bed numbers, dates, medical record numbers, or case IDs.
- Drug doses, procedural orders, or operational treatment instructions.
- Claims that replace local protocols, validated guidelines, or clinician judgment.

If the source material is based on a real case, rewrite it as a generalized teaching scenario before visual generation.

## Recommended Three-skill Workflow

Use the skills as a small production pipeline:

1. `scientific-cover-visual`: create a high-impact teaching cover for a lecture, article, or slide deck.
2. `scientific-infographic`: turn the topic into a structured review or teaching overview.
3. `scientific-paper-figure`: create mechanism-first workflow figures for care pathways, anatomy, injury patterns, or decision flow.

This separation keeps each image focused. The cover creates attention, the infographic explains the topic, and the paper figure clarifies sequence or mechanism.

## Example Topic: Initial Trauma Assessment

For a generic emergency trauma teaching module, the visual set could include:

| Output | Primary skill | Educational use |
| --- | --- | --- |
| Trauma care teaching cover | `scientific-cover-visual` | Slide opener, article header, course cover. |
| Initial assessment overview | `scientific-infographic` | Teaching summary of assessment domains. |
| CABCDE pathway figure | `scientific-paper-figure` | Workflow-style figure for sequence and reassessment logic. |
| Imaging and consultation map | `scientific-infographic` | Teaching matrix for communication and handoff concepts. |

## Prompt Pattern

```text
$scientific-paper-figure
Create an educational emergency trauma workflow figure for initial assessment.
Figure type: workflow / paper-style teaching figure.
Field: emergency medicine and trauma education.
Core structure: CABCDE sequence with repeated reassessment.
Process: catastrophic hemorrhage screen, airway assessment, breathing assessment, circulation assessment, disability assessment, exposure and environment control, then loop back to reassessment.
Output: a clear conceptual pathway for teaching the assessment sequence.
Visual elements: trauma bay silhouette, numbered pathway, loop arrow for reassessment, small insets for airway, breathing, circulation, neurologic check, and exposure.
Language: English short labels.
Aspect ratio: 16:9.
Style: restrained medical atlas palette, clean paper-figure layout.
Forbidden elements: no real patient, no hospital logo, no clinician names, no case ID, no drug doses, no procedural commands, no claim that this is clinical guidance.
Final note: educational use only, not clinical guidance.
```

## Adapting Markdown Knowledge-base Content

When adapting a Markdown clinical teaching page, first reduce it to visual slots:

- Topic: one sentence.
- Audience: learners, clinicians in teaching context, or research communication audience.
- Visual goal: cover, overview, workflow, mechanism, or matrix.
- Core modules: 3-7 short educational concepts.
- Source status: guideline summary, local teaching note, de-identified case discussion, or personal learning note.
- Safety boundary: educational use only, not clinical guidance.

Avoid pasting long clinical notes into an image prompt. Summarize and de-identify first, then let the skill build the visual structure.

## Quality Gate

Before generating or publishing an image, check that:

- The figure is clearly labeled as educational.
- No patient or institution can be identified.
- The visual explains concepts rather than issuing patient-specific instructions.
- Arrows and sequence labels support teaching logic.
- Any medical claims should be reviewed against appropriate guidelines or textbooks before use in formal teaching.
