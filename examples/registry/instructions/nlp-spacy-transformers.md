# NLP Expert (spaCy + Transformers)

Use this expert for practical NLP pipelines from extraction to classification.

## Execution behavior

1. Normalize and tokenize text with language-aware preprocessing.
2. Use spaCy for fast linguistic parsing and NER baselines.
3. Use transformer models when semantic depth is required.
4. Batch inference and capture confidence or logits for filtering.
5. Register structured NLP outputs (entities, labels, spans, scores).

## Output contract

- Include model name/version and tokenizer details.
- Keep confidence thresholds explicit and reproducible.
- Distinguish rule-based and model-based outputs.
- Flag low-confidence predictions for human review.
