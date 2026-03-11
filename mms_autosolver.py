#!/usr/bin/env python3
"""
Auto-solver for https://www1.mms.is/malid/
Supports all three sections:
  1 – Fallorð        (https://www1.mms.is/malid/fallord/)
  2 – Sagnorð        (https://www1.mms.is/malid/sagnord/)
  3 – Óbeygjanleg orð (https://www1.mms.is/malid/obeygjanleg/)

Run with: /tmp/pwenv/bin/python3 mms_autosolver.py
"""

import asyncio
import sys
from playwright.async_api import async_playwright

# ── Exercise lists ────────────────────────────────────────────────────────────

FALLORD_EXERCISES = [
    # (category, name, dataFun, dataPath)
    # ── Nafnorð ───────────────────────────────────────────────────────────
    ("Sérnöfn og samnöfn",          "Verkefni 1", "DragDrop2",  "data/n1.json"),
    ("Sérnöfn og samnöfn",          "Verkefni 2", "DragDrop2",  "data/n2.json"),
    ("Stór eða lítill stafur",      "Verkefni 1", "Dropdown2",  "data/n3.json"),
    ("Kyn",                         "Verkefni 1", "DragDrop2",  "data/n4.json"),
    ("Kyn",                         "Verkefni 2", "DragDrop2",  "data/n5.json"),
    ("Eintala og fleirtala",        "Verkefni 1", "Input5",     "data/n6.json"),
    ("Eintala og fleirtala",        "Verkefni 2", "Clickable1", "data/n7.json"),
    ("Eintala og fleirtala",        "Verkefni 3", "DragDrop2",  "data/n8.json"),
    ("Eintala og fleirtala",        "Verkefni 4", "Dropdown4",  "data/n9.json"),
    ("Fallbeyging",                 "Verkefni 1", "Input2",     "data/n10.json"),
    ("Fallbeyging",                 "Verkefni 2", "Input2",     "data/n11.json"),
    ("Fallbeyging",                 "Verkefni 3", "Input2",     "data/n12.json"),
    ("Fallbeyging",                 "Verkefni 4", "Input4",     "data/n13.json"),
    ("Greinir",                     "Verkefni 1", "DragDrop2",  "data/n14.json"),
    ("Greinir",                     "Verkefni 2", "Input4",     "data/n15.json"),
    ("Veik og sterk beyging",       "Verkefni 1", "DragDrop2",  "data/n14.json"),
    ("Veik og sterk beyging",       "Verkefni 2", "DragDrop2",  "data/n18.json"),
    ("Kenniföll",                   "Verkefni 1", "Input6",     "data/n19.json"),
    ("Hlutstæð og óhlutstæð",       "Verkefni 1", "DragDrop6",  "data/n20.json"),
    ("Stofn",                       "Verkefni 1", "Input3",     "data/n21.json"),
    ("Stofn",                       "Verkefni 2", "Input6",     "data/n22.json"),
    ("Kyn, tala og fall",           "Verkefni 1", "Dropdown5",  "data/n16.json"),
    # ── Greinir ───────────────────────────────────────────────────────────
    ("Viðskeyttur greinir",         "Verkefni 1", "Dropdown1",  "data/g1.json"),
    ("Viðskeyttur greinir",         "Verkefni 2", "Input3",     "data/g2.json"),
    ("Viðskeyttur greinir",         "Verkefni 3", "Input4",     "data/g3.json"),
    ("Laus greinir",                "Verkefni 1", "Input2",     "data/g4.json"),
    ("Laus og viðskeyttur greinir", "Verkefni 1", "Input1",     "data/g5.json"),
    # ── Lýsingarorð ───────────────────────────────────────────────────────
    ("Kyn (LO)",                    "Verkefni 1", "DragDrop2",  "data/l1.json"),
    ("Kyn (LO)",                    "Verkefni 2", "Input4",     "data/l2.json"),
    ("Eintala og fleirtala (LO)",   "Verkefni 1", "DragDrop2",  "data/l3.json"),
    ("Fallbeyging (LO)",            "Verkefni 1", "Input2",     "data/l4.json"),
    ("Fallbeyging (LO)",            "Verkefni 2", "Input2",     "data/l5.json"),
    ("Stigbreyting",                "Verkefni 1", "Input7",     "data/l6.json"),
    ("Stigbreyting",                "Verkefni 2", "Input7",     "data/l7.json"),
    ("Stigbreyting",                "Verkefni 3", "DragDrop2",  "data/l8.json"),
    ("Stigbreyting",                "Verkefni 4", "DragDrop2",  "data/l9.json"),
    ("Stigbreyting",                "Verkefni 5", "Clickable1", "data/l10.json"),
    ("Stigbreyting",                "Verkefni 6", "Dropdown2",  "data/l11.json"),
    ("Stofn (LO)",                  "Verkefni 1", "Input3",     "data/l13.json"),
    ("Sterk og veik beyging (LO)",  "Verkefni 1", "DragDrop6",  "data/l14.json"),
    ("Stig, kyn, tala og fall",     "Verkefni 1", "DragDrop5",  "data/l12.json"),
    ("Orðaforði",                   "Verkefni 1", "Dropdown4",  "data/l15.json"),
    # ── Fornöfn ───────────────────────────────────────────────────────────
    ("Persónufornöfn",              "Verkefni 1", "DragDrop2",  "data/f1.json"),
    ("Persónufornöfn",              "Verkefni 2", "DragDrop6",  "data/f2.json"),
    ("Persónufornöfn",              "Verkefni 3", "Input4",     "data/f3.json"),
    ("Persónufornöfn",              "Verkefni 4", "DragDrop4",  "data/f4.json"),
    ("Persónufornöfn",              "Verkefni 5", "Input4",     "data/f5.json"),
    ("Eignarfornöfn",               "Verkefni 1", "Input2",     "data/f6.json"),
    ("Eignarfornöfn",               "Verkefni 2", "Clickable1", "data/f7.json"),
    ("Eignarfornöfn",               "Verkefni 3", "Input4",     "data/f8.json"),
    ("Eignarfornöfn",               "Verkefni 4", "Input2",     "data/f9.json"),
    ("Ábendingarfornöfn",           "Verkefni 1", "Clickable1", "data/f10.json"),
    ("Spurnarfornöfn",              "Verkefni 1", "Input4",     "data/f11.json"),
    ("Afturbeygð fornöfn",          "Verkefni 1", "Input4",     "data/f12.json"),
    ("Óákveðin fornöfn",            "Verkefni 1", "Input4",     "data/f13.json"),
    ("Óákveðin fornöfn",            "Verkefni 2", "Input2",     "data/f14.json"),
    ("Óákveðin fornöfn",            "Verkefni 3", "Clickable1", "data/f15.json"),
    ("Allir flokkar",               "Verkefni 1", "DragDrop6",  "data/f16.json"),
    ("Allir flokkar",               "Verkefni 2", "DragDrop6",  "data/f17.json"),
    # ── Blönduð ───────────────────────────────────────────────────────────
    ("Fallorð - allir undirflokkar","Verkefni 1", "DragDrop3",  "data/y1.json"),
    ("Fallorð - allir undirflokkar","Verkefni 2", "DragDrop6",  "data/y2.json"),
    ("Fallorð - allir undirflokkar","Verkefni 3", "DragDrop6",  "data/y3.json"),
    ("Fallorð - allir undirflokkar","Verkefni 4", "Input4",     "data/y4.json"),
    ("Fallorð - allir undirflokkar","Verkefni 5", "Input4",     "data/y5.json"),
    # ── Töluorð ───────────────────────────────────────────────────────────
    ("Náttúrulegar tölur og raðtölur","Verkefni 1","DragDrop2", "data/t1.json"),
    ("Náttúrulegar tölur og raðtölur","Verkefni 2","DragDrop6", "data/t2.json"),
    ("Náttúrulegar tölur og raðtölur","Verkefni 3","Input4",    "data/t3.json"),
]

SAGNORD_EXERCISES = [
    # ── Nútíð og þátíð ────────────────────────────────────────────────────
    ("Nútíð og þátíð",              "Verkefni 1", "DragDrop2",  "data/s8.json"),
    ("Nútíð og þátíð",              "Verkefni 2", "DragDrop2",  "data/s9.json"),
    ("Nútíð og þátíð",              "Verkefni 3", "Input4",     "data/s10.json"),
    ("Nútíð og þátíð",              "Verkefni 4", "Input4",     "data/s11.json"),
    ("Nútíð og þátíð",              "Verkefni 5", "Input4",     "data/s12.json"),
    ("Nútíð og þátíð",              "Verkefni 6", "Input14",    "data/s79.json"),
    ("Núliðin-, þáliðin- og framtíð","Verkefni 1","Input2",     "data/s13.json"),
    ("Núliðin-, þáliðin- og framtíð","Verkefni 2","Dropdown7",  "data/s14.json"),
    # ── Eintala og fleirtala ──────────────────────────────────────────────
    ("Eintala og fleirtala",        "Verkefni 1", "Dropdown4",  "data/s15.json"),
    ("Eintala og fleirtala",        "Verkefni 2", "DragDrop2",  "data/s16.json"),
    ("Eintala og fleirtala",        "Verkefni 3", "DragDrop2",  "data/s17.json"),
    # ── Þekkja sagnorð ────────────────────────────────────────────────────
    ("Þekkja sagnorð",              "Verkefni 1", "Clickable1", "data/n7.json"),
    ("Þekkja sagnorð",              "Verkefni 2", "DragDrop4",  "data/s2.json"),
    ("Þekkja sagnorð",              "Verkefni 3", "DragDrop4",  "data/s3.json"),
    ("Þekkja sagnorð",              "Verkefni 4", "DragDrop4",  "data/s3b.json"),
    ("Þekkja sagnorð",              "Verkefni 5", "DragDrop4b", "data/s4.json"),
    ("Þekkja sagnorð",              "Verkefni 6", "Clickable2", "data/s80.json"),
    # ── Stofn ─────────────────────────────────────────────────────────────
    ("Stofn",                       "Verkefni 1", "Input5",     "data/s5.json"),
    ("Stofn",                       "Verkefni 2", "Input5",     "data/s6.json"),
    ("Stofn",                       "Verkefni 3", "Input6",     "data/s7.json"),
    # ── Persónur sagnorða ─────────────────────────────────────────────────
    ("Persónur sagnorða",           "Verkefni 1", "Input8",     "data/s18.json"),
    ("Persónur sagnorða",           "Verkefni 2", "Input8",     "data/s19.json"),
    ("Persónur sagnorða",           "Verkefni 3", "Input4",     "data/s21.json"),
    ("Persónur sagnorða",           "Verkefni 4", "Dropdown7",  "data/s22.json"),
    ("Persónur sagnorða",           "Verkefni 5", "DragDrop4c", "data/s23.json"),
    # ── Ópersónulegar sagnir ──────────────────────────────────────────────
    ("Ópersónulegar sagnir",        "Verkefni 1", "DragDrop2",  "data/s24.json"),
    ("Ópersónulegar sagnir",        "Verkefni 2", "DragDrop2",  "data/s25.json"),
    ("Ópersónulegar sagnir",        "Verkefni 3", "Dropdown4",  "data/s26.json"),
    ("Ópersónulegar sagnir",        "Verkefni 4", "Clickable1", "data/s27.json"),
    ("Ópersónulegar sagnir",        "Verkefni 5", "Clickable1", "data/s28.json"),
    # ── Myndir / Persónuhættir / Fallhættir ───────────────────────────────
    ("Myndir",                      "Verkefni 1", "Dropdown4",  "data/s29.json"),
    ("Persónuhættir",               "Verkefni 1", "Input4",     "data/s30.json"),
    ("Persónuhættir",               "Verkefni 2", "Input9",     "data/s31.json"),
    ("Persónuhættir",               "Verkefni 3", "Dropdown4",  "data/s32.json"),
    ("Persónuhættir",               "Verkefni 4", "Input4",     "data/s33.json"),
    ("Persónuhættir",               "Verkefni 5", "Input13",    "data/s78.json"),
    ("Persónuhættir",               "Verkefni 6", "Input6",     "data/s35.json"),
    ("Persónuhættir",               "Verkefni 7", "Input4",     "data/s36.json"),
    ("Fallhættir",                  "Verkefni 1", "Input4",     "data/s37.json"),
    ("Fallhættir",                  "Verkefni 2", "Input5",     "data/s38.json"),
    ("Fallhættir",                  "Verkefni 3", "Input6",     "data/s41.json"),
    ("Fallhættir",                  "Verkefni 4", "Input2",     "data/s42.json"),
    ("Fallhættir",                  "Verkefni 5", "Input4",     "data/s43.json"),
    ("Fallhættir",                  "Verkefni 6", "Input4",     "data/s44.json"),
    ("Fallhættir",                  "Verkefni 7", "Input4",     "data/s45.json"),
    ("Fallhættir",                  "Verkefni 8", "Clickable1", "data/s46.json"),
    ("Fallhættir",                  "Verkefni 9", "Clickable1", "data/s47.json"),
    ("Fallhættir",                  "Verkefni 10","Input4",     "data/s48.json"),
    # ── Hættir blandað ────────────────────────────────────────────────────
    ("Hættir blandað",              "Verkefni 1", "Dropdown7",  "data/s49.json"),
    ("Hættir blandað",              "Verkefni 2", "Input4",     "data/s50.json"),
    ("Hættir blandað",              "Verkefni 3", "Input4",     "data/s51.json"),
    ("Hættir blandað",              "Verkefni 4", "Dropdown7",  "data/s39.json"),
    ("Hættir blandað",              "Verkefni 5", "Dropdown7",  "data/s40.json"),
    # ── Kennimyndir ───────────────────────────────────────────────────────
    ("Kennimyndir veikra sagna",    "Verkefni 1", "Input6",     "data/s57.json"),
    ("Kennimyndir veikra sagna",    "Verkefni 2", "Input4",     "data/s54.json"),
    ("Kennimyndir sterkra sagna",   "Verkefni 1", "Input10",    "data/s55.json"),
    ("Kennimyndir sterkra sagna",   "Verkefni 2", "Input4",     "data/s56.json"),
    ("Kennimyndir núþálegra sagna", "Verkefni 1", "Input12",    "data/s53.json"),
    ("Kennimyndir núþálegra sagna", "Verkefni 2", "Input11",    "data/s58.json"),
    ("Kennimyndir núþálegra sagna", "Verkefni 3", "Input10",    "data/s59.json"),
    # ── Veikar og sterkar sagnir ──────────────────────────────────────────
    ("Veikar og sterkar sagnir",    "Verkefni 1", "DragDrop2",  "data/s52.json"),
    ("Veikar og sterkar sagnir",    "Verkefni 2", "Input4",     "data/s60.json"),
    ("Veikar og sterkar sagnir",    "Verkefni 3", "Input8",     "data/s61.json"),
    ("Veikar og sterkar sagnir",    "Verkefni 4", "Input4",     "data/s63.json"),
    ("Veikar og sterkar sagnir",    "Verkefni 5", "Input4",     "data/s64.json"),
    # ── Áhrifssögn / Hjálparsögn ──────────────────────────────────────────
    ("Orsakasagnir",                "Verkefni 1", "Input11",    "data/s62.json"),
    ("Sjálfstæð/ósjálfstæð sögn",  "Verkefni 1", "Dropdown7",  "data/s65.json"),
    ("Samsett og ósamsett sögn",    "Verkefni 1", "Dropdown5",  "data/s73.json"),
    ("Áhrifssögn og andlag",        "Verkefni 1", "DragDrop6",  "data/s66.json"),
    ("Áhrifssögn og andlag",        "Verkefni 2", "DragDrop7",  "data/s67.json"),
    ("Áhrifslausar sagnir og sagnfylling","Verkefni 1","Clickable1","data/s68.json"),
    ("Áhrifslausar sagnir og sagnfylling","Verkefni 2","Clickable1","data/s69.json"),
    ("Áhrifslausar og áhrifssagnir","Verkefni 1", "DragDrop2",  "data/s70.json"),
    ("Áhrifslausar og áhrifssagnir","Verkefni 2", "Dropdown5",  "data/s71.json"),
    ("Áhrifslausar og áhrifssagnir","Verkefni 3", "Dropdown5",  "data/s72.json"),
    ("Hjálparsögn og aðalsögn",     "Verkefni 1", "Clickable1", "data/s74.json"),
    ("Hjálparsögn og aðalsögn",     "Verkefni 2", "Clickable1", "data/s75.json"),
    ("Hjálparsögn og aðalsögn",     "Verkefni 3", "Input4",     "data/s76.json"),
    ("Hjálparsögn og aðalsögn",     "Verkefni 4", "Dropdown7",  "data/s77.json"),
]

OBEYGJANLEG_EXERCISES = [
    ("Nafnháttarmerki",        "Verkefni 1", "Clickable1",  "data/n1.json"),
    ("Nafnháttarmerki",        "Verkefni 2", "Clickable1",  "data/n2.json"),
    ("Upphrópun",              "Verkefni 1", "Clickable1",  "data/n3.json"),
    ("Skammstöfun",            "Verkefni 1", "Clickable1",  "data/n41.json"),
    ("Skammstöfun",            "Verkefni 2", "DragDrop4d",  "data/n42.json"),
    ("Forsetningar",           "Verkefni 1", "Clickable1",  "data/n4.json"),
    ("Forsetningar",           "Verkefni 2", "Clickable1",  "data/n5.json"),
    ("Forsetningar",           "Verkefni 3", "DragDrop6",   "data/n6.json"),
    ("Forsetningar",           "Verkefni 4", "Dropdown5",   "data/n8.json"),
    ("Forsetningar",           "Verkefni 5", "Dropdown7",   "data/n10.json"),
    ("Forsetningar",           "Verkefni 6", "Input10",     "data/n52.json"),
    ("Samtengingar",           "Verkefni 1", "Clickable1",  "data/n11.json"),
    ("Samtengingar",           "Verkefni 2", "Clickable1",  "data/n12.json"),
    ("Samtengingar",           "Verkefni 3", "Dropdown7",   "data/n13.json"),
    ("Hljóðbreytingar",        "Verkefni 1", "Dropdown5",   "data/n50.json"),
    ("Hljóðbreytingar",        "Verkefni 2", "Input4",      "data/n51.json"),
    ("Hljóðbreytingar",        "Verkefni 3", "Clickable2",  "data/n53.json"),
    ("Atviksorð",              "Verkefni 1", "Clickable1",  "data/n14.json"),
    ("Atviksorð",              "Verkefni 2", "Clickable1",  "data/n15.json"),
    ("Atviksorð",              "Verkefni 3", "DragDrop4",   "data/n18.json"),
    ("Atviksorð",              "Verkefni 4", "Dropdown5",   "data/n19.json"),
    ("Atviksorð",              "Verkefni 5", "Dropdown8",   "data/n20.json"),
    ("Atviksorð",              "Verkefni 6", "Input4",      "data/n21.json"),
    ("Atviksorð",              "Verkefni 7", "Clickable1",  "data/n22.json"),
    ("Atviksorð",              "Verkefni 8", "Input4",      "data/n23.json"),
    ("Atviksorð",              "Verkefni 9", "Input4",      "data/n24.json"),
    ("Orðflokkagreining",      "Verkefni 1", "Dropdown5",   "data/n16.json"),
    ("Orðflokkagreining",      "Verkefni 2", "Dropdown7",   "data/n17.json"),
    ("Orðflokkagreining",      "Verkefni 3", "Dropdown7",   "data/n25.json"),
    ("Orðflokkagreining",      "Verkefni 4", "Dropdown7",   "data/n26.json"),
    ("Orðflokkagreining",      "Verkefni 5", "Dropdown7",   "data/n27.json"),
    ("Orðflokkagreining",      "Verkefni 6", "Dropdown7",   "data/n28.json"),
    ("Orðflokkagreining",      "Verkefni 7", "Dropdown7",   "data/n29.json"),
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

SECTIONS = {
    "1": ("Fallorð",          "https://www1.mms.is/malid/fallord/",     FALLORD_EXERCISES),
    "2": ("Sagnorð",          "https://www1.mms.is/malid/sagnord/",     SAGNORD_EXERCISES),
    "3": ("Óbeygjanleg orð",  "https://www1.mms.is/malid/obeygjanleg/", OBEYGJANLEG_EXERCISES),
}


# ── Fill-script factory ───────────────────────────────────────────────────────

def get_fill_script(data_fun: str, data_path: str) -> str:
    """Return a JS arrow function that fills the exercise with correct answers."""

    # ── Clickable1 / Clickable2 ───────────────────────────────────────────
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

    # ── Input4/5: inputs carry correct answer in [data] attr ─────────────
    if data_fun in ("Input4", "Input5"):
        return """() => {
            document.querySelectorAll('input[data]').forEach(el => {
                const c = el.getAttribute('data');
                if (c && c !== 'end') el.value = c;
            });
        }"""

    # ── Dropdown1/2/4/5/7/8: select carries correct in [data] attr ───────
    if data_fun in ("Dropdown1", "Dropdown2", "Dropdown4", "Dropdown5", "Dropdown7", "Dropdown8"):
        return """() => {
            document.querySelectorAll('select[data]').forEach(el => {
                el.value = el.getAttribute('data');
                el.dispatchEvent(new Event('change', {bubbles: true}));
            });
        }"""

    # ── DragDrop4 variants (4/4b/4c/4d/4e): droppable slots have [data] ──
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

    # ── DragDrop1 ─────────────────────────────────────────────────────────
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

    # ── DragDrop2 ─────────────────────────────────────────────────────────
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

    # ── DragDrop3: items in wrong boxes, drag to correct category ─────────
    if data_fun == "DragDrop3":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const movable = d.data.filter(i => i.correct !== '-');
            const total = movable.length;
            let added = 0;
            for (const item of movable) {{
                const ul = document.getElementById(item.correct + '-drop');
                if (ul) {{
                    const li = document.createElement('li');
                    li.className = 'DragDrop3-draggable-list showRightAnswers Right';
                    li.setAttribute('data', item.correct);
                    li.textContent = item.drag;
                    ul.appendChild(li);
                    added++;
                }}
            }}
            const score = Math.round((added / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = added + ' / ' + total;
        }}"""

    # ── DragDrop6 ─────────────────────────────────────────────────────────
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

    # ── DragDrop5: drag words into table + pick stig/kyn/tala/fall ────────
    if data_fun == "DragDrop5":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const table = document.querySelector('.DragDrop5-table');
            if (!table) return;
            const total = d.data.length * 4;
            let right = 0;
            for (let i = 0; i < d.data.length; i++) {{
                const item = d.data[i];
                const row = document.createElement('div');
                row.id = 'dropped' + i;
                row.className = 'table-row';
                row.innerHTML = '<div class="droppedText">' + item.draggable + '</div>';
                ['stig','kyn','tala','fall'].forEach((attr, j) => {{
                    const span = document.createElement('span');
                    span.className = 'dropdown-select showRightAnswers Right';
                    span.textContent = item.correct[j] || '';
                    row.appendChild(span);
                    if (item.correct[j]) right++;
                }});
                table.appendChild(row);
            }}
            const score = Math.round((right / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = right + ' / ' + total;
        }}"""

    # ── DragDrop7: drag words into table + pick case (1 attribute) ────────
    if data_fun == "DragDrop7":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            const table = document.querySelector('.DragDrop5-table');
            if (!table) return;
            const validItems = d.data.filter(i => i.draggable && i.draggable.trim() !== '');
            const total = validItems.length;
            let right = 0;
            for (let i = 0; i < d.data.length; i++) {{
                const item = d.data[i];
                if (!item.draggable || !item.draggable.trim()) continue;
                const row = document.createElement('div');
                row.id = 'dropped' + i;
                row.className = 'table-row';
                row.innerHTML = '<div class="droppedText">' + item.draggable + '</div>';
                const span = document.createElement('span');
                span.className = 'dropdown-select showRightAnswers Right';
                span.textContent = (item.correct && item.correct[0]) || '';
                row.appendChild(span);
                if (item.correct && item.correct[0]) right++;
                table.appendChild(row);
            }}
            const score = Math.round((right / total * 100) * 10) / 10;
            document.getElementById('ScoreBar-score').textContent = score + '%';
            document.getElementById('ScoreBar-tries').textContent = right + ' / ' + total;
        }}"""

    # ── Input1: userInput{i} → single string ─────────────────────────────
    if data_fun == "Input1":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInput' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input2/7: userInput-{i}-{j} → array ──────────────────────────────
    if data_fun in ("Input2", "Input7"):
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const correct = d.data[i].correct;
                for (let j = 0; j < correct.length; j++) {{
                    const el = document.getElementById('userInput-' + i + '-' + j);
                    if (el) el.value = correct[j];
                }}
            }}
        }}"""

    # ── Input3: userInput{i} → array (first value suffices) ──────────────
    if data_fun == "Input3":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInput' + i);
                if (el) {{
                    const c = d.data[i].correct;
                    el.value = Array.isArray(c) ? c[0] : c;
                }}
            }}
        }}"""

    # ── Input6: userInput{i}0, userInput{i}1 → array[2] ──────────────────
    if data_fun == "Input6":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                for (let j = 0; j < d.data[i].correct.length; j++) {{
                    const el = document.getElementById('userInput' + i + j);
                    if (el) el.value = d.data[i].correct[j];
                }}
            }}
        }}"""

    # ── Input8/9/11/12: userInput{i}{j} → array ──────────────────────────
    if data_fun in ("Input8", "Input9", "Input11", "Input12"):
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                for (let j = 0; j < d.data[i].correct.length; j++) {{
                    const el = document.getElementById('userInput' + i + j);
                    if (el) el.value = d.data[i].correct[j];
                }}
            }}
        }}"""

    # ── Input10: userInput{i}{j} → array (3 inputs / row) ────────────────
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

    # ── Input13: userInputSpecial{i} ─────────────────────────────────────
    if data_fun == "Input13":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputSpecial' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input14: userInputS{i} ────────────────────────────────────────────
    if data_fun == "Input14":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputS' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input15/17: userInputK{i} ─────────────────────────────────────────
    if data_fun in ("Input15", "Input17"):
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputK' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input16: userInputSb{i} ───────────────────────────────────────────
    if data_fun == "Input16":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputSb' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    # ── Input18: userInputD{i} ────────────────────────────────────────────
    if data_fun == "Input18":
        return f"""async () => {{
            const d = await fetch('{data_path}').then(r => r.json());
            for (let i = 0; i < d.data.length; i++) {{
                const el = document.getElementById('userInputD' + i);
                if (el) el.value = d.data[i].correct;
            }}
        }}"""

    return f"() => {{ console.warn('No fill script for {data_fun}'); }}"


# ── Core solver ───────────────────────────────────────────────────────────────

async def solve_exercise(page, category: str, name: str, data_fun: str, data_path: str) -> str:
    print(f"  [{data_fun:12s}] {category} / {name} ...", end=" ", flush=True)

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

    await page.wait_for_timeout(2000)

    fill_js = get_fill_script(data_fun, data_path)
    await page.evaluate(fill_js)
    await page.wait_for_timeout(400)

    try:
        await page.click("#ScoreBar-checkButton", timeout=2000)
        await page.wait_for_timeout(500)
    except Exception:
        pass

    score = (await page.locator("#ScoreBar-score").text_content() or "?").strip()
    print(score)
    return score


async def run_section(section_name: str, base_url: str, exercises: list):
    print(f"\n{'=' * 65}")
    print(f"  MMS Málið í Mark — {section_name}")
    print(f"  {base_url}")
    print(f"{'=' * 65}")

    results = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, args=["--no-sandbox"])
        page = await (await browser.new_context()).new_page()

        print("\nLoading page...")
        await page.goto(base_url, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        print("Page loaded.\n")

        prev_category = None
        for category, name, data_fun, data_path in exercises:
            if category != prev_category:
                print(f"\n── {category} ──")
                prev_category = category
            score = await solve_exercise(page, category, name, data_fun, data_path)
            results.append((category, name, data_fun, score))

        await browser.close()

    print(f"\n{'=' * 65}")
    print("  RESULTS SUMMARY")
    print(f"{'=' * 65}")
    total = 0.0
    count = 0
    for category, name, fun, score in results:
        mark = "✓" if score == "100%" else "·"
        print(f"  {mark}  {category:<32s} {name:<12s} → {score}")
        try:
            total += float(score.replace("%", ""))
            count += 1
        except ValueError:
            pass

    if count:
        print(f"\n  Average: {total/count:.1f}%  over {count} exercises")
    print("=" * 65)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  MMS Málið í Mark — Auto-Solver")
    print("=" * 65)
    print()
    print("  Select a section:")
    print("    1  –  Fallorð         (67 exercises)")
    print("    2  –  Sagnorð         (79 exercises)")
    print("    3  –  Óbeygjanleg orð (53 exercises)")
    print()

    choice = input("  Your choice (1/2/3): ").strip()

    if choice not in SECTIONS:
        print(f"  Invalid choice '{choice}'. Enter 1, 2, or 3.")
        sys.exit(1)

    section_name, base_url, exercises = SECTIONS[choice]
    asyncio.run(run_section(section_name, base_url, exercises))


if __name__ == "__main__":
    main()
