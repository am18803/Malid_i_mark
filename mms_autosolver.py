#!/usr/bin/env python3
"""
Auto-solver for https://www1.mms.is/malid/obeygjanleg/
Automatically fills in all quiz exercises and submits answers.
Run with: /tmp/pwenv/bin/python3 mms_autosolver.py
"""

import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://www1.mms.is/malid/obeygjanleg/"

EXERCISES = [
    # (category, name, dataFun, dataPath)
    # ── Nafnháttur, upphrópun o.fl. ──────────────────────────────────────
    ("Nafnháttarmerki",        "Verkefni 1", "Clickable1",  "data/n1.json"),
    ("Nafnháttarmerki",        "Verkefni 2", "Clickable1",  "data/n2.json"),
    ("Upphrópun",              "Verkefni 1", "Clickable1",  "data/n3.json"),
    ("Skammstöfun",            "Verkefni 1", "Clickable1",  "data/n41.json"),
    ("Skammstöfun",            "Verkefni 2", "DragDrop4d",  "data/n42.json"),
    # ── Forsetningar ─────────────────────────────────────────────────────
    ("Forsetningar",           "Verkefni 1", "Clickable1",  "data/n4.json"),
    ("Forsetningar",           "Verkefni 2", "Clickable1",  "data/n5.json"),
    ("Forsetningar",           "Verkefni 3", "DragDrop6",   "data/n6.json"),
    ("Forsetningar",           "Verkefni 4", "Dropdown5",   "data/n8.json"),
    ("Forsetningar",           "Verkefni 5", "Dropdown7",   "data/n10.json"),
    ("Forsetningar",           "Verkefni 6", "Input10",     "data/n52.json"),
    # ── Samtengingar og hljóðbreytingar ──────────────────────────────────
    ("Samtengingar",           "Verkefni 1", "Clickable1",  "data/n11.json"),
    ("Samtengingar",           "Verkefni 2", "Clickable1",  "data/n12.json"),
    ("Samtengingar",           "Verkefni 3", "Dropdown7",   "data/n13.json"),
    ("Hljóðbreytingar",        "Verkefni 1", "Dropdown5",   "data/n50.json"),
    ("Hljóðbreytingar",        "Verkefni 2", "Input4",      "data/n51.json"),
    ("Hljóðbreytingar",        "Verkefni 3", "Clickable2",  "data/n53.json"),
    # ── Atviksorð ────────────────────────────────────────────────────────
    ("Atviksorð",              "Verkefni 1", "Clickable1",  "data/n14.json"),
    ("Atviksorð",              "Verkefni 2", "Clickable1",  "data/n15.json"),
    ("Atviksorð",              "Verkefni 3", "DragDrop4",   "data/n18.json"),
    ("Atviksorð",              "Verkefni 4", "Dropdown5",   "data/n19.json"),
    ("Atviksorð",              "Verkefni 5", "Dropdown8",   "data/n20.json"),
    ("Atviksorð",              "Verkefni 6", "Input4",      "data/n21.json"),
    ("Atviksorð",              "Verkefni 7", "Clickable1",  "data/n22.json"),
    ("Atviksorð",              "Verkefni 8", "Input4",      "data/n23.json"),
    ("Atviksorð",              "Verkefni 9", "Input4",      "data/n24.json"),
    # ── Orðflokkagreining ────────────────────────────────────────────────
    ("Orðflokkagreining",      "Verkefni 1", "Dropdown5",   "data/n16.json"),
    ("Orðflokkagreining",      "Verkefni 2", "Dropdown7",   "data/n17.json"),
    ("Orðflokkagreining",      "Verkefni 3", "Dropdown7",   "data/n25.json"),
    ("Orðflokkagreining",      "Verkefni 4", "Dropdown7",   "data/n26.json"),
    ("Orðflokkagreining",      "Verkefni 5", "Dropdown7",   "data/n27.json"),
    ("Orðflokkagreining",      "Verkefni 6", "Dropdown7",   "data/n28.json"),
    ("Orðflokkagreining",      "Verkefni 7", "Dropdown7",   "data/n29.json"),
    # ── Ýmislegt ─────────────────────────────────────────────────────────
    ("Bein og óbein ræða",     "Verkefni 1", "DragDrop4d",  "data/n30.json"),
    ("Samheiti og andheiti",   "Verkefni 1", "DragDrop4",   "data/n35.json"),
    ("Samheiti og andheiti",   "Verkefni 2", "Input14",     "data/n36.json"),
    ("Samheiti og andheiti",   "Verkefni 3", "DragDrop4",   "data/n37.json"),
    ("Samheiti og andheiti",   "Verkefni 4", "Input15",     "data/n38.json"),
    ("Nýyrði/tökuorð",         "Verkefni 1", "Dropdown5",   "data/n44.json"),
    ("Nýyrði/tökuorð",         "Verkefni 2", "Input13",     "data/n45.json"),
    ("Nýyrði/tökuorð",         "Verkefni 3", "DragDrop4",   "data/n46.json"),
    ("Málshættir og orðtök",   "Verkefni 1", "DragDrop2",   "data/n47.json"),
    ("Málshættir og orðtök",   "Verkefni 2", "DragDrop4d",  "data/n48.json"),
    ("Málshættir og orðtök",   "Verkefni 3", "Input4",      "data/n49.json"),
    ("Blönduð verkefni",       "Verkefni 1", "DragDrop2",   "data/n31.json"),
    ("Blönduð verkefni",       "Verkefni 2", "DragDrop4",   "data/n32.json"),
    ("Blönduð verkefni",       "Verkefni 3", "DragDrop4b",  "data/n34.json"),
    ("Blönduð verkefni",       "Verkefni 4", "DragDrop4b",  "data/n39.json"),
    ("Blönduð verkefni",       "Verkefni 5", "DragDrop4b",  "data/n40.json"),
    ("Blönduð verkefni",       "Verkefni 6", "DragDrop1",   "data/n43.json"),
    ("Blönduð verkefni",       "Verkefni 7", "Input16",     "data/n54.json"),
    ("Blönduð verkefni",       "Verkefni 8", "Input17",     "data/n55.json"),
    ("Blönduð verkefni",       "Verkefni 9", "Input18",     "data/n56.json"),
]


def get_fill_script(data_fun: str, data_path: str) -> str:
    """Return a JavaScript arrow function (sync or async) that fills the exercise."""

    # ── Clickable: click every span whose data-attr is not '-' ───────────
    if data_fun == "Clickable1":
        return """() => {
            document.querySelectorAll('.Clickable1-clickable').forEach(el => {
                if (el.getAttribute('data') !== '-') el.click();
            });
        }"""

    if data_fun == "Clickable2":
        return """() => {
            document.querySelectorAll('.Clickable2-clickable').forEach(el => {
                if (el.getAttribute('data') !== '-') el.click();
            });
        }"""

    # ── Input4: each input carries its correct answer in [data] attr ─────
    if data_fun == "Input4":
        return """() => {
            document.querySelectorAll('input[data]').forEach(el => {
                const c = el.getAttribute('data');
                if (c && c !== 'end') el.value = c;
            });
        }"""

    # ── Dropdown5 / 7 / 8: select element carries correct in [data] attr ─
    if data_fun in ("Dropdown5", "Dropdown7", "Dropdown8"):
        return """() => {
            document.querySelectorAll('select[data]').forEach(el => {
                el.value = el.getAttribute('data');
                el.dispatchEvent(new Event('change', {bubbles: true}));
            });
        }"""

    # ── DragDrop4 variants: each droppable slot carries correct in [data] ─
    # All variants (4, 4b, 4c, 4d, 4e) share the CSS class 'DragDrop4-droppable'
    if data_fun.startswith("DragDrop4"):
        return """() => {
            document.querySelectorAll('.DragDrop4-droppable[data]').forEach(el => {
                const val = el.getAttribute('data');
                if (val && val !== '-' && val !== 'nodata') {
                    el.textContent = val;
                    el.classList.add('showRightAnswers');
                    el.classList.remove('showWrongAnswers');
                }
            });
        }"""

    # ── DragDrop6: categorise into column ULs ────────────────────────────
    # correct = 'fs'|'fall'|'wrong'; items with 'wrong' are not scored.
    # NOTE: the check-button handler calls .draggable('disable') on our li
    # elements which are not jQuery-UI draggables, causing an error.
    # We therefore calculate and write the score directly here.
    if data_fun == "DragDrop6":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const total = d.data.filter(i => i.correct !== 'wrong').length;
            let added = 0;
            for (const item of d.data) {{
                const cat = item.correct;
                if (cat && cat !== 'wrong' && cat !== '-') {{
                    const ul = document.getElementById(cat + '-drop');
                    if (ul) {{
                        const li = document.createElement('li');
                        li.className = 'DragDrop6-draggable-list showRightAnswers Right';
                        li.setAttribute('data', cat);
                        li.textContent = item.drag;
                        ul.appendChild(li);
                        added++;
                    }}
                }}
            }}
            const score = Math.round((added / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = added + ' / ' + total;
        }}"""

    # ── DragDrop1: multi-column categorisation ───────────────────────────
    # Check handler calls .draggable('disable') on list items → error.
    # Write score directly.
    if data_fun == "DragDrop1":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const total = d.data.filter(i => i.correct !== '-').length;
            let added = 0;
            for (const item of d.data) {{
                const cat = item.correct;
                if (cat && cat !== '-') {{
                    const ul = document.getElementById(cat + '-drop');
                    if (ul) {{
                        const li = document.createElement('li');
                        li.className = 'DragDrop1-draggable-list showRightAnswers Right';
                        li.setAttribute('data', cat);
                        li.textContent = item.drag;
                        ul.appendChild(li);
                        added++;
                    }}
                }}
            }}
            const score = Math.round((added / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = added + ' / ' + total;
        }}"""

    # ── DragDrop2: sequential 2-column categorisation ────────────────────
    # Same issue — write score directly.
    if data_fun == "DragDrop2":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const total = d.data.length;
            let added = 0;
            for (const item of d.data) {{
                const cat = item.correct;
                if (cat && cat !== '-') {{
                    const ul = document.getElementById(cat + '-drop');
                    if (ul) {{
                        const li = document.createElement('li');
                        li.className = 'DragDrop2-draggable-list showRightAnswers Right';
                        li.setAttribute('data', cat);
                        li.textContent = item.drag;
                        ul.appendChild(li);
                        added++;
                    }}
                }}
            }}
            const score = Math.round((added / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = added + ' / ' + total;
        }}"""

    # ── Input10: 3 inputs per row (preposition, noun, case) ───────────────
    # IDs: userInput{i}0, userInput{i}1, userInput{i}2
    if data_fun == "Input10":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                for (let j = 0; j < d.data[i].correct.length; j++) {{
                    const el = document.getElementById('userInput' + i + j);
                    if (el) el.value = d.data[i].correct[j];
                }}
            }}
        }}"""

    # ── Input13: crossword, IDs: userInputSpecial{i} ─────────────────────
    if data_fun == "Input13":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputSpecial' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input14: crossword, IDs: userInputS{i} ───────────────────────────
    if data_fun == "Input14":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputS' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input15 / Input17: crossword, IDs: userInputK{i} ─────────────────
    if data_fun in ("Input15", "Input17"):
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputK' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input16: crossword, IDs: userInputSb{i} ──────────────────────────
    if data_fun == "Input16":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputSb' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input18: crossword, IDs: userInputD{i} ───────────────────────────
    if data_fun == "Input18":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputD' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # Fallback
    return f"() => {{ console.warn('No fill script for {data_fun}'); }}"


async def solve_exercise(page, category: str, name: str, data_fun: str, data_path: str) -> str:
    """Load an exercise, fill in correct answers, click check, return score."""
    print(f"  [{data_fun:12s}] {category} / {name} ...", end=" ", flush=True)

    # Clear content, unbind all accumulated score-bar handlers, call handler
    await page.evaluate(f"""() => {{
        try {{ clearInterval(window.interval); }} catch(e) {{}}
        try {{ $('#ScoreBar-checkButton').off('click'); }} catch(e) {{}}
        try {{ $('#ScoreBar-retry').off('click'); }} catch(e) {{}}
        const a = document.getElementById('Assignment');
        a.innerHTML = '';
        a.style.backgroundImage = 'none';
        document.getElementById('ScoreBar-score').textContent = '0%';
        try {{ {data_fun}("{data_path}"); }} catch(e) {{ console.error(e); }}
    }}""")

    # Wait for JSON fetch + DOM build (async XHR + jQuery rendering)
    await page.wait_for_timeout(2000)

    # Fill in the correct answers
    fill_js = get_fill_script(data_fun, data_path)
    await page.evaluate(fill_js)
    await page.wait_for_timeout(400)

    # Click the check button
    try:
        await page.click("#ScoreBar-checkButton", timeout=2000)
        await page.wait_for_timeout(500)
    except Exception:
        pass

    # Read and return the score
    score = (await page.locator("#ScoreBar-score").text_content() or "?").strip()
    print(score)
    return score


async def main():
    print("=" * 65)
    print("  MMS Málið í Mark — Auto-Solver")
    print("  https://www1.mms.is/malid/obeygjanleg/")
    print("=" * 65)

    results: list[tuple[str, str, str, str]] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,       # set True to hide the browser window
            args=["--no-sandbox"],
        )
        page = await (await browser.new_context()).new_page()

        print("\nLoading page...")
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        print("Page loaded.\n")

        prev_category = None
        for category, name, data_fun, data_path in EXERCISES:
            if category != prev_category:
                print(f"\n── {category} ──")
                prev_category = category
            score = await solve_exercise(page, category, name, data_fun, data_path)
            results.append((category, name, data_fun, score))

        await browser.close()

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  RESULTS SUMMARY")
    print("=" * 65)
    total = 0.0
    count = 0
    for category, name, fun, score in results:
        mark = "✓" if score == "100%" else "·"
        print(f"  {mark}  {category:<28s} {name:<12s} → {score}")
        try:
            total += float(score.replace("%", ""))
            count += 1
        except ValueError:
            pass

    if count:
        print(f"\n  Average: {total/count:.1f}%  over {count} exercises")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(main())
