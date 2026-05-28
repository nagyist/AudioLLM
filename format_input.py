import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import os
import numpy as np

# Load JSON files from the 'items' folder
model_cards = []
folder_path = 'items'
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r') as f:
            model_cards.append(json.load(f))

# Convert the time strings to datetime objects (include months)
times = [datetime.strptime(card["Time"], "%Y-%m") for card in model_cards]
labels = [card["Abbreviation"] for card in model_cards]

# Group model cards by month
grouped_cards = {}
for card, time in zip(model_cards, times):
    month = time.strftime('%Y-%m')
    if month not in grouped_cards:
        grouped_cards[month] = []
    grouped_cards[month].append(card)

# Sort grouped cards by most recent month first
grouped_cards = dict(sorted(grouped_cards.items(), reverse=True))

# Set up the plot
fig, ax = plt.subplots(figsize=(12, len(grouped_cards) * 2))  # Reduced width of the figure

# Plot the timeline with items listed vertically
y_pos = 0
yticks = []
ytick_labels = []
for month, cards in grouped_cards.items():
    for card in cards:
        label = f"**{card['Abbreviation']}**"
        card_type = card.get("Type", "Unknown Type")
        audio_in = "Audio In" if card.get("Audio_Input", "No") == "Yes" else ""
        audio_out = "Audio Out" if card.get("Audio_Output", "No") == "Yes" else ""
        language = "Multilingual" if card.get('Language', 'Unknown') == 'Multilingual' else card.get('Language', 'Unknown')

        # Build formatted text
        formatted_text_parts = [label, f"Type: {card_type}"]
        if audio_in:
            formatted_text_parts.append(audio_in)
        if audio_out:
            formatted_text_parts.append(audio_out)
        if language:
            formatted_text_parts.append(language)
        formatted_text = ", ".join(filter(None, formatted_text_parts))

        # Add text to the plot
        ax.text(1.05, y_pos, formatted_text, ha="left", va="center", fontsize=10, color="black", weight="bold")
        y_pos -= 1

    # Add month label
    yticks.append(y_pos + len(cards) / 2)
    ytick_labels.append(month)
    y_pos -= 1  # Add space between months

# Set the y-axis ticks and labels
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels)

# Adjust the plot
ax.get_xaxis().set_visible(False)
ax.set_xlim(0.95, 2.0)
ax.set_ylim(y_pos, 1)
plt.tight_layout()

# Save the plot locally
plt.savefig('model_release_timeline_vertical_listed.png', dpi=300)

# Group cards by category for README generation
categories = {}
for card in model_cards:
    category = card.get("Category", "Uncategorized")
    if category not in categories:
        categories[category] = []
    categories[category].append(card)

# Sort models within each category by time
def sort_by_time(card):
    return datetime.strptime(card["Time"], "%Y-%m")

for category in categories:
    categories[category].sort(key=sort_by_time, reverse=True)

# Generate README.md content
readme_lines = []
# ============== Platform-style hero ==============
readme_lines.append("# 🎧 audio-ai-hub")
readme_lines.append("")
readme_lines.append("**The hub for audio AI research.** Curated papers, open models, benchmarks and datasets across audio LLMs · speech recognition · speech synthesis · music & audio generation.")
readme_lines.append("")
# Stats line, computed below after we know totals
_total = len(model_cards)
_n_cat = len(categories)
_latest = max(card["Time"] for card in model_cards)
readme_lines.append(f"`{_total} entries` · `{_n_cat} categories` · `latest: {_latest}`")
readme_lines.append("")
readme_lines.append("👉 **[Interactive site (search & filter)](https://binwang28.github.io/audio-ai-hub/)** · **[Contribute](CONTRIBUTING.md)** · **[Suggest a paper](https://github.com/BinWang28/audio-ai-hub/issues/new?template=add-paper.yml)**")
readme_lines.append("")
readme_lines.append("---")
readme_lines.append("")
# Contributors
readme_lines.append("## Contributors")
readme_lines.append("We thank the following contributors for their valuable contributions!")
readme_lines.append("[zwenyu](https://github.com/zwenyu), ")
readme_lines.append("[Yuan-ManX](https://github.com/Yuan-ManX), ")
readme_lines.append("[chaoweihuang](https://github.com/chaoweihuang), ")
readme_lines.append("[Liu-Tianchi](https://github.com/Liu-Tianchi), ")
readme_lines.append("[Sakshi113](https://github.com/Sakshi113), ")
readme_lines.append("[hbwu-ntu](https://github.com/hbwu-ntu), ")
readme_lines.append("[potsawee](https://github.com/potsawee), ")
readme_lines.append("[czwxian](https://github.com/czwxian), ")
readme_lines.append("[marianasignal](https://github.com/marianasignal), ")
readme_lines.append("and You!")

readme_lines.append("[![Star History Chart](https://api.star-history.com/svg?repos=BinWang28/audio-ai-hub&type=Date)](https://star-history.com/#BinWang28/audio-ai-hub&Date)")



# ================== Add the Table of Contents ==================
readme_lines.append("## Table of Contents")
for category in categories:
    anchor = category.lower().replace(" ", "-")
    readme_lines.append(f"- [{category}](#{anchor})")
readme_lines.append("")

readme_lines.append('<img src="model_release_timeline_vertical_listed.png" alt="Timeline Visualization" width="600">')  # Embed smaller image
readme_lines.append("")

# Add a list of abbreviations with links
readme_lines.append("### Abbreviations with Links")
model_cards.sort(key=lambda card: datetime.strptime(card["Time"], "%Y-%m"), reverse=True)

for card in model_cards:
    abbreviation = card["Abbreviation"]
    paper_link = card.get("Paper_Link", "")
    hf_link = card.get("HF_Link", "")
    demo_link = card.get("Demo_Link", "")
    github_link = card.get("GitHub_Link", "")
    other_link = card.get("Other_Link", "")

    # Create a link (default to the paper link, then other available links)
    link = paper_link or hf_link or demo_link or github_link or other_link
    if link:
        readme_lines.append(f"- [{abbreviation}]({link})")
    else:
        readme_lines.append(f"- {abbreviation} (No link available)")

readme_lines.append("")  # Add spacing before categories

for category, cards in categories.items():
    readme_lines.append(f"## {category}\n")
    for card in cards:
        abbreviation = card["Abbreviation"]
        title = card.get("Title", "No title available")
        affiliation = card.get("Affiliation", "Unknown affiliation")
        author = card.get("Author", "Unknown authors")
        card_type = card.get("Type", "Unknown Type")
        paper_link = card.get("Paper_Link", "")
        hf_link = card.get("HF_Link", "")
        demo_link = card.get("Demo_Link", "")
        github_link = card.get("GitHub_Link", "")
        other_link = card.get("Other_Link", "")

        links = []
        if paper_link:
            links.append(f"[Paper]({paper_link})")
        if hf_link:
            links.append(f"[Hugging Face Model]({hf_link})")
        if demo_link:
            links.append(f"[Demo]({demo_link})")
        if other_link:
            links.append(f"[Other Link]({other_link})")

        github_shield = f"[![GitHub stars](https://img.shields.io/github/stars/{'/'.join(github_link.split('/')[-2:])}?style=social)]({github_link})" if github_link else ""

        readme_lines.append(f"- `【{card['Time']}】-【{abbreviation}】-【{affiliation}】-【Type: {card_type}】`")
        readme_lines.append(f"  - **{title}**")
        readme_lines.append(f"  - **Author(s):** {author}")
        if github_shield:
            readme_lines.append(f"  - {github_shield}")
        if links:
            readme_lines.append(f"  - {' / '.join(links)}")
        readme_lines.append("")

# Write to README.md
with open("README.md", "w") as readme_file:
    readme_file.write("\n".join(readme_lines))


print("README.md has been generated.")

# Emit docs/data.json for the static frontend (GitHub Pages).
# Sorted by Time desc, then Abbreviation asc, so the rendered card grid is stable.
os.makedirs('docs', exist_ok=True)
sorted_cards = sorted(
    model_cards,
    key=lambda c: (datetime.strptime(c["Time"], "%Y-%m"), c.get("Abbreviation", "")),
    reverse=False,
)
sorted_cards.sort(
    key=lambda c: datetime.strptime(c["Time"], "%Y-%m"),
    reverse=True,
)
with open('docs/data.json', 'w', encoding='utf-8') as out:
    json.dump(sorted_cards, out, ensure_ascii=False, indent=2)
print(f"docs/data.json written ({len(sorted_cards)} entries).")


# ============== Server-side render of docs/index.html ==============
# Inject pre-rendered HTML between marker comments so non-JS readers (and
# search engines that skip JS) see the actual content. JS in app.js takes
# over for interactive filtering after page load.
import html as _html
import re as _re

def _h(s):
    return _html.escape(str(s) if s is not None else "", quote=True)

def _slug(s):
    return _re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

# Load star counts (built by scripts/refresh_stars.py)
stars_by_abbrev = {}
if os.path.exists('docs/stars.json'):
    with open('docs/stars.json', encoding='utf-8') as f:
        stars_by_abbrev = {k: v.get('stars', 0) for k, v in json.load(f).items()}

def _card_html(card):
    abbrev = card.get('Abbreviation', '')
    cat = card.get('Category', '')
    cat_slug = _slug(cat)
    links = []
    if card.get('Paper_Link'):
        links.append(f'<a href="{_h(card["Paper_Link"])}" target="_blank" rel="noopener">Paper</a>')
    if card.get('GitHub_Link'):
        links.append(f'<a href="{_h(card["GitHub_Link"])}" target="_blank" rel="noopener">Code</a>')
    if card.get('HF_Link'):
        links.append(f'<a href="{_h(card["HF_Link"])}" target="_blank" rel="noopener">🤗 HF</a>')
    if card.get('Demo_Link'):
        links.append(f'<a href="{_h(card["Demo_Link"])}" target="_blank" rel="noopener">Demo</a>')
    if card.get('Other_Link'):
        links.append(f'<a href="{_h(card["Other_Link"])}" target="_blank" rel="noopener">Site</a>')
    tags = [f'<span class="tag tag-cat" data-cat="{cat_slug}">{_h(cat)}</span>']
    if card.get('Type') and card['Type'] != cat:
        tags.append(f'<span class="tag">{_h(card["Type"])}</span>')
    if card.get('Audio_Input') == 'Yes':
        tags.append('<span class="tag">Audio In</span>')
    if card.get('Audio_Output') == 'Yes':
        tags.append('<span class="tag">Audio Out</span>')
    if card.get('Language') and card['Language'] not in ('-', ''):
        tags.append(f'<span class="tag">{_h(card["Language"])}</span>')
    stars = stars_by_abbrev.get(abbrev, 0)
    star_badge = f'<span class="card-stars" title="GitHub stars">★ {stars:,}</span>' if stars else ''
    affil = card.get('Affiliation', '')
    desc = card.get('Description', '')
    return (
        f'<article class="card" data-abbrev="{_h(abbrev)}" data-cat="{cat_slug}" data-stars="{stars}">'
        f'<header class="card-head"><span class="card-abbrev">{_h(abbrev)}</span>'
        f'<span class="card-time">{_h(card.get("Time", ""))}</span></header>'
        f'<p class="card-title">{_h(card.get("Title", ""))}</p>'
        + (f'<p class="card-affil">{_h(affil)}</p>' if affil else '')
        + f'<div class="tags">{"".join(tags)}{star_badge}</div>'
        + (f'<p class="card-desc">{_h(desc)}</p>' if desc else '')
        + f'<footer class="card-links">{"".join(links)}</footer>'
        '</article>'
    )

# Featured = top 8 by stars (entries with no Github link are excluded from featured)
featured = [c for c in sorted_cards if stars_by_abbrev.get(c.get('Abbreviation', ''), 0) > 0]
featured.sort(key=lambda c: -stars_by_abbrev.get(c.get('Abbreviation', ''), 0))
featured = featured[:8]
featured_html = '\n'.join(_card_html(c) for c in featured)

# Main grid: all entries, newest first (sorted_cards already in that order)
grid_html = '\n'.join(_card_html(c) for c in sorted_cards)

# Stats line
total = len(sorted_cards)
n_cats = len({c.get('Category', '') for c in sorted_cards})
latest = max(c.get('Time', '') for c in sorted_cards) if sorted_cards else '—'
stats_html = (
    f'<div class="stat"><strong>{total}</strong>entries</div>'
    f'<div class="stat"><strong>{n_cats}</strong>categories</div>'
    f'<div class="stat"><strong>{latest}</strong>latest</div>'
)

# Category chips, ordered the same way the README sections are ordered
cat_counts = {}
for c in sorted_cards:
    cat_counts[c.get('Category', '')] = cat_counts.get(c.get('Category', ''), 0) + 1
preferred_order = [
    "Model and Methods", "Speech Recognition", "Speech Synthesis",
    "Audio Generation", "Benchmark", "Dataset Resource", "Multimodal",
    "Survey", "Study", "Safety", "Chatbot",
]
ordered_cats = [c for c in preferred_order if c in cat_counts] + \
               [c for c in cat_counts if c not in preferred_order]
chips_html = ''.join(
    f'<button class="chip" type="button" data-category="{_h(c)}" data-cat="{_slug(c)}" aria-pressed="false">'
    f'{_h(c)}<span class="count">{cat_counts[c]}</span></button>'
    for c in ordered_cats
)

# Inject into docs/index.html between marker pairs
with open('docs/index.html', encoding='utf-8') as f:
    page = f.read()

def _inject(html_text, marker, content):
    pattern = _re.compile(
        rf'(<!-- {marker}-START -->).*?(<!-- {marker}-END -->)',
        flags=_re.DOTALL,
    )
    return pattern.sub(lambda m: m.group(1) + content + m.group(2), html_text)

page = _inject(page, 'AUTO-STATS', stats_html)
page = _inject(page, 'AUTO-CATEGORY-FILTER', chips_html)
page = _inject(page, 'AUTO-FEATURED', featured_html)
page = _inject(page, 'AUTO-GRID', grid_html)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(page)
print(f"docs/index.html SSR'd (featured: {len(featured)}, grid: {len(sorted_cards)}).")
