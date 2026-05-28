# Contributing to Awesome-Audio-LLM

Thanks for wanting to add a paper, model, or benchmark to the list! `README.md` is **generated** from JSON files in `items/` by `format_input.py`, so the contribution workflow is JSON-first, not README-first.

## Scope

This list focuses on **audio-LLM research artifacts**:

- Papers and technical reports (audio/speech foundation models, audio-language models, multimodal LLMs with an audio modality)
- Open model releases (HuggingFace, GitHub) tied to research
- Benchmarks and datasets for audio LLMs
- Surveys, safety and evaluation studies in the audio-LLM space

Out of scope:

- Commercial products without an associated paper or open model
- General TTS/STT tools, voice assistants, and consumer apps unrelated to LLM research
- SEO/promotional submissions

## How to add a new item

### 1. Create `items/<Abbreviation>.json`

Use this template (every field is required; leave a string empty if it does not apply):

```json
{
    "Category":     "Model and Methods",
    "Type":         "Model",
    "Abbreviation": "SPIRIT LM",
    "Title":        "SPIRIT LM: Interleaved Spoken and Written Language Model",
    "Time":         "2024-10",
    "Affiliation":  "Meta",
    "Author":       "Tu Anh Nguyen, Benjamin Muller, ...",
    "GitHub_Link":  "https://github.com/facebookresearch/spiritlm",
    "Paper_Link":   "https://arxiv.org/abs/2402.05755",
    "HF_Link":      "",
    "Demo_Link":    "https://speechbot.github.io/spiritlm/",
    "Other_Link":   "",
    "Audio_Input":  "Yes",
    "Audio_Output": "Yes",
    "Language":     "English",
    "Description":  "One- to two-sentence summary of what the work does."
}
```

Field conventions:

- **`Category`** — one of: `Model and Methods`, `Benchmark`, `Dataset Resource`, `Safety`, `Multimodal`, `Survey`, `Study`, `Chatbot`. These render as top-level sections in the README.
- **`Type`** — short descriptor (`Model`, `Benchmark`, `Survey`, `Dataset Resource`, `Method`, `Research`, etc.). Free-form, but try to match existing entries.
- **`Abbreviation`** — short canonical name (e.g. `SPIRIT LM`, `Audio Flamingo 2`). It is used as the visible label and to look up the entry. The JSON filename should match this slug.
- **`Time`** — `YYYY-MM` of the arXiv submission or release. Used to sort the timeline image and the README.
- **`Audio_Input` / `Audio_Output`** — `Yes` or `No`. Used for the timeline annotation.
- **`Language`** — `English`, `Multilingual`, a specific language name, or empty.

### 2. Regenerate `README.md` and the timeline image

```bash
python3 format_input.py
```

This rewrites `README.md` and `model_release_timeline_vertical_listed.png` from all `items/*.json` files. Commit the regenerated files alongside your new JSON.

### 3. Open a pull request

Include in the PR:

- the new `items/<Abbreviation>.json`
- the regenerated `README.md`
- the regenerated `model_release_timeline_vertical_listed.png`

A README-only PR cannot be merged cleanly — the next regeneration would erase the change. PRs that include the JSON file are easy to merge.

## Suggesting an item without filing a PR

If you do not want to write a PR yourself, open an issue with the JSON template filled in and a maintainer will add it. Please include the arXiv link and a one-sentence description; that is usually enough to extract the rest.

## Closing notes

If you find an existing entry with wrong metadata (typo, wrong year, wrong link), please open a PR that edits the corresponding `items/*.json` file directly and re-runs `format_input.py`.
