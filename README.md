# MMS Málið í Mark — Auto-Solver

Automatically solves all exercises on [https://www1.mms.is/malid/](https://www1.mms.is/malid/) — an Icelandic grammar quiz site. Covers all three sections with 199 exercises total.

## Requirements

Python 3 with Playwright. If you haven't set it up yet:

```bash
python3 -m venv ~/pwenv
~/pwenv/bin/pip install playwright
~/pwenv/bin/playwright install chromium
```

## Running

```bash
~/pwenv/bin/python3 mms_autosolver.py
```

You will be prompted to pick a section:

```
  Select a section:
    1  –  Fallorð         (67 exercises)
    2  –  Sagnorð         (79 exercises)
    3  –  Óbeygjanleg orð (53 exercises)

  Your choice (1/2/3):
```

A browser window opens, the script fills every exercise automatically, then prints a full score summary.

## How it works

The site is entirely client-side. Each exercise loads a JSON file (`data/nX.json`) and renders into a `#Assignment` div using one of ~20 JavaScript exercise functions. The correct answers are embedded in that same JSON data.

The script works in three steps for each exercise:

**1. Load** — calls the site's own exercise function directly via `page.evaluate`, e.g. `Clickable1("data/n1.json")`. This builds the exercise DOM exactly as a real user would see it.

**2. Fill** — injects a small JavaScript snippet that reads the correct answers from the DOM or re-fetches the JSON, then fills in the answers:

| Exercise type | How answers are stored | Fill method |
|---|---|---|
| `Clickable1/2` | `data` attribute on each span | Programmatically `.click()` the correct spans |
| `Input4/5` | `data` attribute on each `<input>` | Set `el.value = el.getAttribute('data')` |
| `Dropdown1/2/4/5/7/8` | `data` attribute on each `<select>` | Set `el.value` and dispatch `change` event |
| `DragDrop4` (all variants) | `data` attribute on droppable slots | Set slot text + add `showRightAnswers` class |
| `DragDrop1/2/3/6` | JSON: `item.correct` = category ID | Create `<li>` elements in correct category `<ul>` |
| `DragDrop5/7` | JSON: `item.correct` = attribute array | Build table rows with correct values marked |
| `Input1/3` | JSON: `data[i].correct` (string/array) | Fill `userInput{i}` by index |
| `Input2/7` | JSON: `data[i].correct` (array) | Fill `userInput-{i}-{j}` by row+column |
| `Input6/8/9/11/12` | JSON: `data[i].correct` (array) | Fill `userInput{i}{j}` by row+column |
| `Input10/13–18` | JSON: `data[i].correct` | Fill named inputs (`userInputSpecial`, `userInputK`, etc.) |

**3. Score** — clicks the check button (`#ScoreBar-checkButton`). For drag-drop types where the check handler crashes (because our JS-created elements aren't jQuery UI draggables), the fill script writes the score directly to `#ScoreBar-score` instead.

## Screenshots

After each exercise the script takes a full-page screenshot and saves it automatically. When you run the script it asks where to save them:

```
  Where to save screenshots?
  Press Enter for default: /home/<you>/Desktop/app/screenshots/<Section name>
  Save to:
```

Press **Enter** to use the default folder, or type a custom path. Screenshots are named like:

```
Fallorð__Verkefni_1__100_0%.png
```

You can browse all screenshots in your file manager or any image viewer.

## Results

| Section | Exercises | Typical average |
|---|---|---|
| Óbeygjanleg orð | 53 | 99.4% |
| Fallorð | 67 | ~95%+ |
| Sagnorð | 79 | ~95%+ |

One exercise (Blönduð verkefni / Verkefni 8 in Óbeygjanleg orð) has a design ceiling of 68.8% because 5 of 16 answer slots are pre-filled by the site but still counted in the denominator.

## License

MIT License

Copyright (c) 2025 am18803

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
