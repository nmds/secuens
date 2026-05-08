# Contributing to Secuens

Thank you for your interest in contributing to the Secuens specification.

---

## What This Repository Contains

This repository holds the **Secuens specification** — an open plain-text format for technical cue notation in production documents.

It does not contain application code. If you're looking to build a tool that implements Secuens, see the [Implementations](https://www.secuens.org/implementations) page.

---

## Branch Structure

- **`main`** — stable releases only. Do not open PRs directly against `main`.
- **`draft`** — active development branch. All contributions go here.

When contributing, always open Pull Requests against the `draft` branch.

---

## Ways to Contribute

### Report Specification Issues

If you find ambiguities, edge cases, or errors in the specification:

1. Open an [Issue](https://github.com/nmds/secuens/issues)
2. Use the label `spec-issue`
3. Describe the specific section, the problem, and (if possible) a proposed resolution

### Suggest Improvements

If you have ideas for:

- New standard metadata keys
- Domain-specific cue type conventions
- New trigger keyword patterns
- Future version features

Open an Issue with the label `enhancement` and describe your use case from real production experience.

### Improve Examples

If you have real-world production examples that demonstrate edge cases or domain-specific workflows:

1. Fork the repository
2. Add your example to `specification/v0.9/examples/` following the naming convention: `domain-description.secuens`
3. Open a Pull Request against the `draft` branch with a brief description of what the example demonstrates

### Fix Documentation

Typos, unclear wording, broken links — open a Pull Request against the `draft` branch.

---

## What We're Looking For

Secuens is a specification for practitioners. The most valuable contributions come from:

- **Stage managers** and **production managers** who work with cue notation daily
- **Assistant directors** and **script supervisors** in film and television
- **Technical directors** and **show callers** in live events and broadcast
- **Developers** building tools that parse or generate Secuens documents

If you work in production and find something that doesn't match how you actually work, that's valuable feedback.

---

## What We're Not Looking For

- Requests to change the core syntax to accommodate a specific tool's limitations
- Features that solve problems better handled at the application layer
- Spec changes that would break backward compatibility without strong justification

---

## Specification Philosophy

Before submitting a contribution, please read the [Design Principles](specification/v0.9/Secuens-v0.9.1-DRAFT.md#design-principles) in the spec. Contributions should align with:

- **Plain-text first** — the spec must remain readable in any text editor
- **Domain-agnostic** — changes should work across theatre, film, broadcast, and beyond
- **Progressive enhancement** — simple cues should stay simple; complexity is opt-in
- **Parser-friendly** — syntax must be unambiguous and reliably parseable

---

## Process

This is a small, focused project. There's no formal governance structure yet. Significant changes to the specification will be discussed openly in Issues and Discussions before being incorporated.

The specification maintainer is [@nmds](https://github.com/nmds).

---

## License

By contributing to this repository, you agree that your contributions will be licensed under the same [CC BY-ND 4.0](LICENSE) license that covers the specification.

Note: CC BY-ND 4.0 covers the specification document itself. Example files and tools in this repository may be under different licenses as noted in their respective directories.
