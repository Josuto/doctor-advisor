# Red flags are detected by two layers over one normalised catalogue, not by retrieval

Red flags are defined once, in a normalised catalogue: condition-specific red flags are referenced by id from `conditions.yaml`, and general ones live in `general_red_flags.yaml`. Each is a combination of required findings with lay phrasings. Detection fires on the union of two layers:
- a deterministic lemma-based phrase matcher, which fires when all of a red flag's findings are present and also reports near misses;
- a separate Red Flag Check agent run, in parallel with triage, that receives the whole catalogue as a cached prompt prefix to catch paraphrases.

We rejected a red-flag vector index. A retrieval miss would be a silent emergency miss, and embeddings handle "all findings present" and negation poorly. This brings back the similarity-threshold problem in the most safety-critical place.

## Consequences

- The catalogue's token budget (default 30k) is an app setting checked at startup. If it's exceeded, the app refuses to start. Growth past it is handled by presentation-first narrowing (classify the emergency presentation, then check only its red flags), never by flat retrieval. Narrowing may only be adopted if it keeps 100% recall on the red-flag eval.
- Red flags are not embedded in the conditions RAG index.
- False positives caused by negation ("no chest pain") are accepted.
