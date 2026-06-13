---
name: paper-to-essay
description: Convert a technical research paper into an accessible, well-written essay for educated non-expert readers. The essay explains and describes the paper's points and concepts clearly without requiring expertise in mathematics, physics, or technology. Optionally generates illustrative images. Use when the user says "convert this paper to an essay", "make this readable for non-experts", "write a layperson version", "explain this paper to a general audience", "magazine version", "humanities version", or "accessible version" of a research paper.
---

# Paper to Essay

Converts a technical paper in `docnav/Research/papers/` into an accessible narrative essay for educated non-experts.

## Output location

All essays go in `docnav/Research/papers/essays/`, named:

```
<N>_<original-slug>_<audience>.md
```

**Audience labels** (ask the user if not specified):

| Label | Target reader |
|---|---|
| `educated-layperson` | Thoughtful adult with no specialist background |
| `magazine` | General-interest science/culture magazine |
| `humanities` | Academic in the humanities; comfortable with ideas, not equations |
| `highschool` | Bright secondary-school student |

## Step 1: Read the source paper

Read the full source `.md` file from `docnav/Research/papers/`.

## Step 2: Determine the audience

If not specified, ask the user which audience label to use. The audience determines tone, vocabulary level, and how much the essay can assume.

## Step 3: Write the essay

Apply every rule below. Do not structure the essay like the original paper. Do not reproduce section numbers, abstract headers, or numbered lists from the source.

### Title and deck

- Write a new title that would attract a curious non-expert. It should convey the *stakes or surprise* of the paper, not its technical name.
- Follow with a one-sentence deck (subtitle) that describes what the essay argues and why it matters.
- Add an attribution line:
  - For `educated-layperson` and `humanities`: `*An essay for educated readers outside the mathematical sciences*`
  - For `magazine`: `*By J. W. Milton, Clarity Coalition*`
  - For `highschool`: `*An introduction for curious students*`

### Body structure

- Use `---` horizontal rules and short bold headers to divide sections, never numbered headings.
- Opening: begin with a concrete scene, surprising fact, or provocative question. No jargon in the first three paragraphs.
- Each major concept from the paper gets: (1) a plain-English statement of what it is, (2) an analogy or everyday example, (3) why it matters.
- Replace all equations with prose descriptions. If an equation is genuinely central, describe what it *does*, not what it *says*.
- Replace jargon with the most accurate plain-English substitute. On first use, give the jargon in parentheses if it may appear again.
- Never use em dashes. Use commas, colons, or new sentences.
- Never say "the author argues" or "this paper shows." Write directly: "The framework argues," "The evidence shows."
- Occasional pull quotes (a single striking sentence in a `> blockquote`) are encouraged. Use sparingly (one per 500 words at most).

### Ending

Close with what the paper's findings imply for the reader's world. Not a summary of sections. A forward-looking statement of significance.

### Length

Aim for 1,200 to 2,500 words depending on the paper's complexity. The `highschool` audience targets the shorter end. `humanities` and `magazine` may run longer.

## Step 4: Generate images (optional)

If the paper contains diagrams, conceptual figures, or charts that would help non-expert readers, use the `GenerateImage` tool to create illustrative versions.

**Image rules:**
- Create images only when a concept is genuinely hard to grasp in prose alone.
- Style: clean, flat-design illustration or minimal diagram. No photorealism.
- Save location is handled automatically by the `GenerateImage` tool. Reference images in the essay with standard markdown: `![caption](path)`.
- Maximum two images per essay unless the paper is heavily visual.

**Triagram color and position conventions (non-negotiable, apply to every N-D-C diagram):**
- N point: always **blue**, positioned at the **top** vertex of the triangle.
- D point: always **green**, positioned at the **lower right** vertex of the triangle.
- C point: always **red**, positioned at the **lower left** vertex of the triangle.

## Step 5: Save the file

Write the completed essay to:

```
docnav/Research/papers/essays/<N>_<slug>_<audience>.md
```

where `<N>` and `<slug>` match the source paper's filename.

## Style reference

Existing essays in `docnav/Research/papers/essays/` are canonical style examples. Read at least one before writing.

Key characteristics of the existing essays:
- `1_recursive-tholonic-five-constants_magazine.md`: punchy opening, pull quote, analogies for every abstract step, no equations
- `10_tholonic-neural-architecture_educated-layperson.md`: longer narrative arc, journalistic section headers, implications-first framing

## Checklist before saving

- [ ] No numbered section headings from the source paper carried over
- [ ] No LaTeX or raw equations
- [ ] No em dashes anywhere
- [ ] Every abstract claim followed by an analogy or concrete example
- [ ] Title and deck are compelling to a non-specialist
- [ ] File saved to `docnav/Research/papers/essays/`
