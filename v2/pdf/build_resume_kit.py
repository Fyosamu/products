# -*- coding: utf-8 -*-
"""Build: THE RESUME & COVER LETTER KIT 2026 -> HTML -> PDF (Chrome headless)."""
import subprocess
import pathlib

OUT = pathlib.Path(__file__).parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

NAVY = "#1F2A44"
TEAL = "#0FA3B1"
GOLD = "#F4B942"
LIGHT = "#EAF4F4"
GREY = "#8D99AE"
INK = "#2B2F38"

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#fff; color:{INK};
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width:210mm; height:297mm; padding:12mm 12mm 10mm; page-break-after:always;
  position:relative; overflow:hidden; display:flex; flex-direction:column; }}
.page > * {{ flex:0 0 auto; }}
.page:last-child {{ page-break-after:auto; }}

.cover {{ background:{NAVY}; color:#fff; justify-content:space-between; padding:22mm 18mm; }}
.cover h1 {{ font-size:52px; line-height:1.04; margin:0; letter-spacing:-1.4px; font-weight:800; }}
.cover h1 span {{ color:{GOLD}; }}
.cover .kicker {{ font-size:12px; letter-spacing:5px; text-transform:uppercase; color:{TEAL};
  margin-bottom:10mm; font-weight:700; }}
.cover .sub {{ font-size:15px; color:#C9D2E0; margin-top:6mm; line-height:1.65; max-width:130mm; }}
.cover .rule {{ height:3px; width:40mm; background:{GOLD}; margin:8mm 0; }}
.cover .badges {{ display:flex; gap:5mm; flex-wrap:wrap; }}
.cover .badge {{ border:1px solid rgba(255,255,255,.28); border-radius:40px; padding:3mm 5.5mm;
  font-size:10.5px; letter-spacing:.6px; }}
.cover .foot {{ font-size:11px; color:#7E8CA3; letter-spacing:1px; }}

.hdr {{ display:flex; align-items:flex-end; justify-content:space-between;
  border-bottom:2.5px solid {NAVY}; padding-bottom:3mm; margin-bottom:4mm; }}
.hdr h2 {{ font-size:23px; margin:0; color:{NAVY}; letter-spacing:-.4px; font-weight:800; text-transform:uppercase; }}
.hdr .tag {{ font-size:10px; letter-spacing:3px; text-transform:uppercase; color:{TEAL}; font-weight:700; }}
.foot {{ position:absolute; left:12mm; right:12mm; bottom:6mm; display:flex; justify-content:space-between;
  font-size:8px; color:{GREY}; letter-spacing:1.6px; text-transform:uppercase;
  border-top:1px solid #E6EBF0; padding-top:2mm; }}

.cols2 {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; flex:1 1 auto; min-height:0; }}
.cols3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:4.5mm; flex:1 1 auto; min-height:0; }}
.card {{ border:1px solid #D8DFE7; border-radius:2.5mm; padding:3.5mm; display:flex; flex-direction:column; }}
.card h4 {{ margin:0 0 2.5mm; font-size:9.5px; letter-spacing:2.4px; text-transform:uppercase;
  color:{TEAL}; border-bottom:1.5px solid {LIGHT}; padding-bottom:2mm; }}
ul.t {{ margin:0; padding-left:5mm; font-size:10px; line-height:1.7; color:#4A5260; }}
ul.t li::marker {{ color:{TEAL}; }}
ul.t.tight li {{ line-height:1.55; }}
.note {{ background:#FFFDF6; border-left:3px solid {GOLD}; padding:3mm 4mm; font-size:9.5px;
  line-height:1.6; color:#5A6272; border-radius:0 2mm 2mm 0; }}
.pill {{ display:inline-block; background:{LIGHT}; color:{NAVY}; border-radius:30px;
  padding:1.1mm 3.2mm; font-size:8.5px; font-weight:700; margin:0 1.4mm 1.4mm 0; }}
.pill.gold {{ background:{GOLD}; }}

/* ---- resume sheet mock ---- */
.sheet {{ border:1px solid #D8DFE7; border-radius:2mm; background:#fff; padding:6mm 7mm;
  display:flex; flex-direction:column; flex:1 1 auto; min-height:0; box-shadow:0 0 0 3px #F4F7FA; }}
.rname {{ font-size:21px; font-weight:800; color:{NAVY}; letter-spacing:-.4px; }}
.rrole {{ font-size:11px; color:{TEAL}; font-weight:700; letter-spacing:1.7px; text-transform:uppercase; margin-top:1.2mm; }}
.rcontact {{ font-size:8.6px; color:{GREY}; margin-top:2mm; padding-bottom:4mm;
  border-bottom:2px solid {LIGHT}; }}
.rsec {{ font-size:9.2px; font-weight:800; color:{NAVY}; letter-spacing:2.4px; text-transform:uppercase;
  margin:6mm 0 2.6mm; padding-bottom:1.2mm; border-bottom:1px solid #E3E9EF; }}
.rjob {{ display:flex; justify-content:space-between; align-items:baseline; font-size:9.8px; }}
.rjob b {{ color:{NAVY}; font-weight:700; }}
.rjob span {{ color:{GREY}; font-size:8.5px; }}
.rco {{ font-size:9.2px; color:{TEAL}; font-weight:600; margin:.7mm 0 2mm; }}
ul.r {{ margin:0 0 4mm; padding-left:4mm; font-size:9.4px; line-height:1.72; color:#41485A; }}
ul.r li {{ margin-bottom:2.4mm; }}
ul.r li::marker {{ color:{GOLD}; }}
.rtwo {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.rskills {{ font-size:9px; line-height:1.65; color:#41485A; }}
.rskills b {{ color:{NAVY}; }}
.chip {{ display:inline-block; border:1px solid #D6DEE7; border-radius:20px; padding:.6mm 2.4mm;
  font-size:8.3px; margin:0 1.2mm 1.2mm 0; color:#41485A; }}

/* ---- tables ---- */
table.t {{ width:100%; border-collapse:collapse; font-size:9px; }}
table.t th {{ background:{NAVY}; color:#fff; font-size:8px; letter-spacing:1.4px; text-align:left; padding:2mm; }}
table.t td {{ border:1px solid #E3E9EF; padding:1.9mm 2.2mm; vertical-align:top; }}
table.t tr:nth-child(even) td {{ background:#FAFCFD; }}
table.t td:first-child {{ font-weight:700; color:{NAVY}; }}
table.t.teal th {{ background:{TEAL}; }}

.form {{ border:1px solid #D8DFE7; border-radius:2.5mm; padding:3.5mm; background:#FBFDFE; flex:1 1 auto; }}
.form h4 {{ margin:0 0 2.5mm; font-size:9.5px; letter-spacing:2.4px; text-transform:uppercase; color:{TEAL}; }}
.form .lbl {{ font-size:8.5px; font-weight:800; color:{NAVY}; letter-spacing:1.4px;
  text-transform:uppercase; margin:3mm 0 1.2mm; }}
.line {{ border-bottom:1px dotted #C3CBD5; flex:1 1 auto; min-height:5.6mm; }}
.lines {{ display:flex; flex-direction:column; flex:1 1 auto; min-height:0; }}
.code {{ background:{NAVY}; color:#DCE6F2; font-family:Consolas,'Courier New',monospace;
  font-size:8.6px; line-height:1.6; padding:3mm; border-radius:2mm; white-space:pre-wrap; }}
.code b {{ color:{GOLD}; font-weight:700; }}
.code i {{ color:{TEAL}; font-style:normal; }}
.kv {{ display:flex; justify-content:space-between; font-size:9.4px; padding:1.7mm 0;
  border-bottom:1px dotted #C3CBD5; }}
.kv b {{ color:{NAVY}; }}
.g {{ color:#128A5B; }} .r {{ color:#C0392B; }} .a {{ color:{GOLD}; }}
"""

P = []


def foot(l, r):
    return f'<div class="foot"><span>{l}</span><span>{r}</span></div>'


def bullets(items):
    return "<ul class='r'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def page(head, tag, body, l, r):
    P.append(f'<section class="page"><div class="hdr"><h2>{head}</h2>'
             f'<div class="tag">{tag}</div></div>{body}{foot(l, r)}</section>')


# ------------------------------------------------------------------ COVER
P.append(f"""
<section class="page cover">
  <div>
    <div class="kicker">Second edition · 2026</div>
    <h1>THE RESUME &amp;<br>COVER LETTER<br><span>KIT 2026</span></h1>
    <div class="rule"></div>
    <div class="sub">Six proven resume layouts, three cover-letter templates, 60 achievement-bullet
    formulas, 120 power verbs, the ATS checklist and the salary scripts. Every page is a real,
    copy-and-edit document — not advice about documents.</div>
  </div>
  <div>
    <div class="badges">
      <div class="badge">6 RESUME LAYOUTS</div>
      <div class="badge">3 COVER LETTERS</div>
      <div class="badge">60 BULLET FORMULAS</div>
      <div class="badge">ATS-TESTED</div>
    </div>
    <div class="rule" style="margin-top:10mm"></div>
    <div class="foot">INSTANT DOWNLOAD · EDIT IN WORD / GOOGLE DOCS · PERSONAL USE</div>
  </div>
</section>""")

# ------------------------------------------------------------------ START HERE
page("Start here", "Read this first", f"""
<div class="cols2">
  <div class="card">
    <h4>The 4 rules that decide everything</h4>
    <ul class="t">
      <li><b>One page.</b> Two pages only past ~10 years of relevant work, and never three.</li>
      <li><b>No photo, no colour blocks, no icons in the skills list.</b> Applicant tracking
      systems strip them and sometimes read them as garbage.</li>
      <li><b>Every bullet carries a number.</b> "Managed social" is invisible.
      "Grew the newsletter 0 → 18,400 in 9 months" is an interview.</li>
      <li><b>Mirror the job description.</b> If they write "customer success", do not write
      "client happiness". Same words, same scanner, same shortlist.</li>
    </ul>
    <div class="note" style="margin-top:4mm">
      A recruiter spends about <b>7 seconds</b> on the first pass. Design the top third of
      page one so those 7 seconds answer: who you are, what you do, and what you have done.
    </div>
  </div>
  <div class="card">
    <h4>How to use this kit in one sitting</h4>
    <ul class="t">
      <li><b>Step 1 (10 min).</b> Paste the job description into a blank doc. Highlight every
      repeated noun and verb — that is your keyword list.</li>
      <li><b>Step 2 (15 min).</b> Pick a layout on the next pages. Skills-first if you are
      changing careers, compact single-column if you are unsure — it is the safest.</li>
      <li><b>Step 3 (30 min).</b> Rewrite every bullet using the formulas in the Bullet Bank.
      Verbs from the Power Verb list, numbers wherever you can honestly give them.</li>
      <li><b>Step 4 (10 min).</b> Run the ATS checklist. Tick all 24 or fix the ones you missed.</li>
      <li><b>Step 5 (15 min).</b> Adapt a cover letter template. Send both as
      <span style="font-weight:700">Firstname-Lastname-Resume.pdf</span>.</li>
    </ul>
    <div class="note" style="margin-top:4mm">
      <b>Keep a master version.</b> Never edit the master — duplicate it per application and
      change only the top third plus the keywords. That is the whole trick.
    </div>
  </div>
</div>
<div class="cols3" style="margin-top:5mm;flex:0 0 auto">
  <div class="card" style="flex:0 0 auto"><h4>What's inside</h4>
    <span class="pill">6 resume layouts</span><span class="pill">3 cover letters</span>
    <span class="pill">60 bullets</span><span class="pill">120 verbs</span>
    <span class="pill">ATS checklist</span><span class="pill">LinkedIn rewrite</span>
    <span class="pill">Interview answers</span><span class="pill gold">Salary scripts</span>
  </div>
  <div class="card" style="flex:0 0 auto"><h4>File formats</h4>
    <ul class="t tight">
      <li>This PDF is the guide — print it or keep it open.</li>
      <li>Copy the text straight into Word or Google Docs to build the real document.</li>
      <li>Use Calibri, Arial, Garamond or Helvetica at 10–11 pt. Nothing else.</li>
      <li>Export the final as PDF. Never send a .docx unless they ask.</li>
    </ul>
  </div>
  <div class="card" style="flex:0 0 auto"><h4>What not to do</h4>
    <ul class="t tight">
      <li>No "References available on request" — everyone knows.</li>
      <li>No objective statement from 2005. Use a 2-line summary instead.</li>
      <li>No salary history, no marital status, no date of birth.</li>
      <li>Never list a skill you cannot defend for five minutes in an interview.</li>
    </ul>
  </div>
</div>
""", "The Resume & Cover Letter Kit 2026", "02")

# ------------------------------------------------------------------ ATS CHECKLIST
ats = [
    ("File type", "PDF, named Firstname-Lastname-Resume.pdf", "g"),
    ("Length", "One page (unless 10+ years of directly relevant work)", "g"),
    ("Fonts", "Calibri / Arial / Garamond / Helvetica, 10–11 pt", "g"),
    ("Headers & footers", "Empty — many parsers cannot read them", "g"),
    ("Columns", "Single column. Two columns lose 30–40% of parses", "g"),
    ("Tables & text boxes", "None. They break the reading order", "g"),
    ("Images, icons, logos", "None", "g"),
    ("Special characters", "No arrows, stars, emoji, or line-drawing characters", "g"),
    ("Contact block", "Name, city, phone, email, LinkedIn URL — as plain text", "g"),
    ("Email", "Professional, no nicknames or year of birth", "g"),
    ("Job titles", "Exactly as they appear on the posting when you held that title", "g"),
    ("Dates", "Mon YYYY – Mon YYYY (or YYYY – YYYY). Consistent everywhere", "g"),
    ("Keywords", "Every core noun/verb from the JD appears at least once", "g"),
    ("Section headings", "EXPERIENCE, EDUCATION, SKILLS — standard wording", "g"),
    ("Skills section", "Plain list, no rating bars or dot meters", "g"),
    ("Bullets", "3–5 per role, each with a verb and a number", "g"),
    ("Verb tense", "Present for current role, past for previous roles", "g"),
    ("Spelling", "Read it backwards, sentence by sentence", "g"),
    ("Grammar", "No first names, no articles dropped, no fragments", "g"),
    ("Metrics", "At least 6 bullets across the page carry a number", "g"),
    ("Gaps", "Explain anything over 6 months in one honest line", "g"),
    ("Education", "Degree, institution, year. No GPA past 3 years out", "g"),
    ("Formatting check", "Open the PDF and copy-paste it — if text scrambles, rebuild", "g"),
    ("Final test", "Print to paper. If it does not look right on paper it is not done", "g"),
]
ats_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td style='text-align:center'>◻</td></tr>" for a, b, _ in ats)
page("ATS checklist", "24 checks · tick every one", f"""
<div style="font-size:10px;color:#5A6272;margin-bottom:3.5mm">
Applicant tracking systems are dumb readers, not judges. They do not reject you for taste —
they reject you because they could not parse the file. Every row below is a way a real resume
has failed a real screen.
</div>
<table class="t">
  <tr><th style="width:44mm">CHECK</th><th>WHAT "PASS" LOOKS LIKE</th><th style="width:16mm">DONE</th></tr>
  {ats_rows}
</table>
<div class="note" style="margin-top:4mm">
<b>The 60-second self-test:</b> email the PDF to yourself, open it on your phone, and read only
the top third. If you cannot instantly say what job this person wants, so will the recruiter.
</div>
""", "ATS checklist", "03")


# ------------------------------------------------------------------ RESUME LAYOUTS
def contact_line():
    return ('<div class="rcontact">[CITY], [COUNTRY] &nbsp;·&nbsp; [PHONE] &nbsp;·&nbsp; '
            '[EMAIL] &nbsp;·&nbsp; linkedin.com/in/[HANDLE] &nbsp;·&nbsp; [PORTFOLIO IF RELEVANT]</div>')


LAYOUTS = [
    dict(
        n="Layout 1 — Compact single-column", tag="Safest · default choice",
        why="One column, no graphics, parses perfectly in every ATS. Use this if you are
        applying to a large company, or if you are not sure which layout to pick. It is not
        the prettiest — it is the most reliable.",
        name="JORDAN A. MERCER", role="Marketing Manager",
        sections=[
            ("SUMMARY", ["Marketing manager with 6 years turning search and email into
              predictable pipeline. Grew two B2B SaaS newsletters past 20k subscribers and
              cut cost per lead 38% in one year. Comfortable owning budget, agency and roadmap."]),
        ],
        jobs=[
            ("MARKETING MANAGER", "Northwind Software", "2022 — Present",
             ["Own paid search, lifecycle email and the blog for a $14M ARR product; grew
              qualified demos 61% YoY while holding spend flat.",
              "Rebuilt the lifecycle sequence (11 emails); trial-to-paid moved 4.2% → 7.9% in two quarters.",
              "Manage two specialists plus a $480k annual budget and a three-agency roster."]),
            ("MARKETING SPECIALIST", "Brightline Analytics", "2020 — 2022",
             ["Ran the webinar programme: 24 events, 5,900 registrants, 310 sourced opportunities.",
              "Cut cost per lead from $84 to $52 by killing three channels and doubling down on one."]),
        ],
        side=("EDUCATION", "BSc Marketing, University of Leeds, 2020"),
        skills="SEO · Google Ads · HubSpot · GA4 · Lifecycle email · Copywriting · SQL basics · Budget ownership"),
    dict(
        n="Layout 2 — Modern timeline", tag="Best for 3–10 years' experience",
        why="Same parser-friendly structure, but the date column is pulled out to the right so
        the eye can scan tenure instantly. Use it when your career is steady and you want the
        page to feel designed without breaking a single ATS rule.",
        name="PRIYA RAGHUNATHAN", role="Senior Product Designer",
        sections=[
            ("PROFILE", ["Product designer, 7 years, fintech and marketplace. Ships research-to-release
              on small teams. Redesigned a checkout that recovered $1.1M in annual revenue."]),
        ],
        jobs=[
            ("SENIOR PRODUCT DESIGNER", "Kestrel Pay", "2023 — Present",
             ["Led the redesign of a 6-step checkout to 3 steps; abandonment 63% → 41%, ~$1.1M/yr recovered.",
              "Built and documented the design system (84 components) now used by 5 squads.",
              "Runs the weekly critique and mentors two mid-level designers."]),
            ("PRODUCT DESIGNER", "Marketplace Co", "2020 — 2023",
             ["Shipped seller onboarding; activation in the first session rose 27% (n = 41k).",
              "Ran 60+ usability sessions and turned findings into a quarterly experiment backlog."]),
        ],
        side=("EDUCATION", "BDes Interaction Design, NID, 2018"),
        skills="Figma · Design systems · Usability testing · Prototyping · Accessibility (WCAG 2.2) · HTML/CSS literacy"),
    dict(
        n="Layout 3 — Skills-first (career changer)", tag="For switching industries",
        why="When the job titles on your history do not match the job you want, lead with the
        skills that do transfer. The experience section still follows — it just stops being
        the first thing read.",
        name="DANIEL OKONKWO", role="Data Analyst → moving from retail operations",
        sections=[
            ("CORE SKILLS", None),
            ("RELEVANT PROJECTS", None),
        ],
        jobs=[
            ("SHIFT MANAGER", "Halcyon Grocery Group", "2019 — Present",
             ["Built the weekly sales tracker in a spreadsheet the district now uses across 14 stores.",
              "Cut wastage 19% by re-forecasting produce orders from my own 8-week demand model.",
              "Trained 22 staff; halved till-error rate in the first quarter after training."]),
        ],
        side=("EDUCATION", "BSc Economics, University of Lagos, 2017 · Google Data Analytics Certificate, 2025"),
        skills="SQL (joins, CTEs, window functions) · Python (pandas) · Power BI · Excel (Power Query) · A/B testing · Statistics"),
        chips=True,
        projects=[("Demand forecasting model", "Python + pandas on 8 weeks of store data; MAPE 6.4%."),
                  ("Wastage dashboard", "Power BI, refreshed daily; now standard in 14 stores."),
                  ("Checkout queue simulation", "Discrete-event model that justified a second till on Saturdays.")]),
    dict(
        n="Layout 4 — Technical / engineering", tag="Projects beat job titles",
        why="Engineers get screened on stack and shipped work. Put the stack in a scannable
        strip, then let projects and impact carry the page. Keep the education short.",
        name="MIRA TANAKA", role="Backend Engineer",
        sections=[("STACK", None)],
        jobs=[
            ("BACKEND ENGINEER", "Loomstack", "2022 — Present",
             ["Cut p95 API latency 840ms → 190ms by moving session reads to Redis and fixing three N+1 queries.",
              "Designed the idempotent payment webhook that stopped duplicate charges (0 in 14 months).",
              "Own the on-call runbook; MTTR down from 47 to 12 minutes."]),
            ("JUNIOR DEVELOPER", "Cartwheel Labs", "2020 — 2022",
             ["Wrote the CSV import service still handling 40k files/day.",
              "Raised backend test coverage 34% → 81% and wired it into CI."]),
        ],
        side=("EDUCATION", "BSc Computer Science, University of Auckland, 2020"),
        skills="Go · Python · PostgreSQL · Redis · Kafka · Docker · Kubernetes · Terraform · AWS (ECS, RDS, S3) · OpenTelemetry"),
        chips=True),
    dict(
        n="Layout 5 — Graduate / entry level", tag="Under 2 years of experience",
        why="You have no job history, so lead with education, projects, internships and
        anything measurable. Three bullets per item is plenty — padding reads as inexperience.",
        name="TOMÁS HERRERA", role="Junior Financial Analyst — graduate",
        sections=[("EDUCATION", None), ("INTERNSHIP", None), ("PROJECTS", None),
                  ("ACTIVITIES", None)],
        jobs=[],
        side=None,
        skills="Excel (INDEX/MATCH, pivot, Power Query) · Financial modelling · Valuation · Power BI · Python basics",
        grad=True),
    dict(
        n="Layout 6 — Executive / senior leader", tag="10+ years, P&L, board-facing",
        why="One page, but the top third is a leadership summary with scope: revenue, team
        size, geographies. Chronology below is compressed to three lines per role — nobody
        hiring a director needs your 2009 bullet points.",
        name="HELENA VOSS", role="Chief Operating Officer",
        sections=[("LEADERSHIP SUMMARY", None)],
        jobs=[
            ("CHIEF OPERATING OFFICER", "Ridgeline Group", "2021 — Present",
             ["Took a 340-person, 4-country operation from 11% to 24% EBITDA in 3 years.",
              "Integrated two acquisitions (180 staff) with zero regretted attrition in year one."]),
            ("VP OPERATIONS", "Ridgeline Group", "2017 — 2021",
             ["Built the ops function from 6 to 120 people; introduced quarterly OKRs across all teams.",
              "Renegotiated the top 12 suppliers, releasing $4.2M of annualised cost."]),
        ],
        side=("EDUCATION", "MBA, INSEAD, 2012 · BEng, TU Delft, 2006"),
        skills="P&L ownership · M&A integration · Supply chain · Multi-site operations · Board reporting · Change management",
        chips=True),
]

for i, L in enumerate(LAYOUTS, start=4):
    body = [f'<div class="sheet">']
    body.append(f'<div class="rname">{L["name"]}</div>')
    body.append(f'<div class="rrole">{L["role"]}</div>')
    body.append(contact_line())

    for title, payload in L.get("sections", []):
        body.append(f'<div class="rsec">{title}</div>')
        if title in ("CORE SKILLS", "STACK"):
            _skills = L.get("stack") or L["skills"]
            body.append('<div class="rskills">' + "".join(
                f'<span class="chip">{s.strip()}</span>' for s in _skills.split("·")) + "</div>")
        elif title == "EDUCATION" and L.get("grad"):
            body.append(bullets([
                "<b>BSc Finance, University of Barcelona, 2025</b> — 3.7/4.0; final-year thesis on working-capital cycles in SME retail.",
                "<b>Relevant coursework:</b> Corporate valuation, Econometrics, Financial statement analysis, Derivatives.",
                "<b>CFA Level I candidate</b> (Dec 2026 session)."]))
        elif title == "INTERNSHIP":
            body.append("<div class='rco'>Finance Intern · Grupo Meridian · Jun – Sep 2025</div>" + bullets([
                "Prepared the monthly cash forecast for a €40M business unit; found €210k of unclaimed supplier rebates.",
                "Automated a 400-row manual reconciliation with Power Query — 6 hours a week returned to the team.",
                "Presented a pricing analysis to the CFO that changed the discount floor on two product lines."]))
        elif title == "PROJECTS" and L.get("grad"):
            body.append(bullets([
                "<b>Solvency model, 3-year DCF</b> — built from filings for a listed retailer; fair value within 4% of consensus.",
                "<b>Working-capital dashboard</b> — Excel + Power BI tracking DSO/DPO across 9 subsidiaries.",
                "<b>Student fund, treasurer</b> — grew the portfolio €12k → €31k over 18 months with a 6-asset allocation rule."]))
        elif title == "PROJECTS":
            body.append(bullets([f"<b>{t}</b> — {d}" for t, d in L["projects"]]))
        elif title == "ACTIVITIES":
            body.append(bullets([
                "President, Investment Society (2024–25) — 180 members, 12 events, speaker series with 4 alumni in asset management.",
                "CFA Research Challenge — team reached the national final; my write-up scored highest on the judging sheet."]))
        elif title == "SUMMARY" or title == "PROFILE" or title == "LEADERSHIP SUMMARY":
            body.append(f'<ul class="r"><li>{payload[0]}</li></ul>')
        elif title == "RELEVANT PROJECTS":
            body.append(bullets([f"<b>{t}</b> — {d}" for t, d in L["projects"]]))

    if L["jobs"]:
        body.append('<div class="rsec">Experience</div>')
        for title, co, dates, bl in L["jobs"]:
            body.append(f'<div class="rjob"><b>{title}</b><span>{dates}</span></div>')
            body.append(f'<div class="rco">{co}</div>')
            body.append(bullets(bl))

    if L.get("side"):
        t, v = L["side"]
        body.append(f'<div class="rsec">{t}</div>')
        body.append(f'<ul class="r"><li>{v}</li></ul>')

    if not L.get("skip_skills"):
        body.append('<div class="rsec">Skills</div>')
        if L.get("chips"):
            body.append('<div class="rskills">' + "".join(
                f'<span class="chip">{s.strip()}</span>' for s in L["skills"].split("·")) + "</div>")
        else:
            body.append(f'<div class="rskills">{L["skills"]}</div>')
    body.append("</div>")

    why_html = f'<div class="note" style="margin-top:4mm;flex:0 0 auto"><b>When to use it:</b> ' \
               f'{L["why"].replace(chr(10), " ")}</div>'
    page(L["n"], L["tag"], "".join(body) + why_html,
         "Resume layouts", f"{i:02d}")

# ------------------------------------------------------------------ COVER LETTERS
page("Cover letter — the structure", "Template A · the safe one", f"""
<div class="cols2">
  <div class="form">
    <h4>Fill-in-the-bracket version</h4>
    <div class="code">[CITY], [DATE]

[HIRING MANAGER NAME]
[HIRING MANAGER TITLE]
[COMPANY]

Re: [JOB TITLE], ref [REF IF ANY]

Dear [NAME],

<i>Para 1 — the hook.</i> I am applying for the [JOB TITLE]
role. For [N] years I have [ONE SENTENCE OF PROOF, WITH A
NUMBER] — most recently at [CURRENT/LAST COMPANY].

<i>Para 2 — why them.</i> [COMPANY]'s [SPECIFIC THING:
PRODUCT, MOVE, CUSTOMER, RESULT] is why I am writing rather
than clicking apply. [ONE LINE SHOWING YOU DID THE RESEARCH].

<i>Para 3 — the fit.</i> The role asks for [REQUIREMENT 1]
and [REQUIREMENT 2]. I [PROOF FOR 1] and [PROOF FOR 2].
[WORST-CASE CONCERN, ANSWERED IN ONE LINE — gap, relocation,
career change].

<i>Para 4 — the close.</i> I would welcome 20 minutes to
walk through how I would approach [FIRST 90-DAY THING].
I am available [WINDOW] and can be reached on [PHONE].

Thank you for your time,

[YOUR NAME]</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:4mm">
    <div class="card" style="flex:0 0 auto">
      <h4>The four paragraphs, in order</h4>
      <table class="t teal">
        <tr><th>PARA</th><th>JOB</th><th>LENGTH</th></tr>
        <tr><td>1 — Hook</td><td>What you want + your single strongest number</td><td>2 lines</td></tr>
        <tr><td>2 — Why them</td><td>Proof you researched them, not 40 companies</td><td>2–3 lines</td></tr>
        <tr><td>3 — Fit</td><td>Two requirements, two proofs, one concern defused</td><td>3–4 lines</td></tr>
        <tr><td>4 — Close</td><td>Ask for 20 minutes, give a window, give a phone number</td><td>2 lines</td></tr>
      </table>
    </div>
    <div class="card" style="flex:0 0 auto">
      <h4>Hard limits</h4>
      <ul class="t tight">
        <li><b>250–350 words.</b> One page, three-quarters full is the target.</li>
        <li>No "I am writing to express my interest in…" — start with the proof.</li>
        <li>Never write "Dear Sir or Madam". Find the name on LinkedIn or the team page;
        if truly impossible, use "Hiring team".</li>
        <li>One document, one job. Templates are for speed, not for sending identical letters.</li>
        <li>Attach as PDF, named <b>Firstname-Lastname-Cover-Letter.pdf</b>.</li>
      </ul>
    </div>
    <div class="note" style="flex:1 1 auto">
      <b>The research line is the whole letter.</b> "I saw your post about moving the API to
      streaming responses" beats three paragraphs about how passionate you are. It proves you
      would read their docs on day one.
    </div>
  </div>
</div>
""", "Cover letters", "10")

page("Cover letter — two more", "Templates B and C", f"""
<div class="cols2">
  <div class="form">
    <h4>B · The warm / referred letter</h4>
    <div class="code">Dear [NAME],

[CONTACT NAME] suggested I write to you about the
[JOB TITLE] role — they felt my work on [PROJECT] mapped
onto what [TEAM] is doing this year.

At [CURRENT COMPANY] I [ONE RESULT WITH A NUMBER].
Before that I [SECOND RESULT, DIFFERENT SKILL].
The pattern is simple: [ONE LINE THAT SUMMARISES HOW YOU WORK].

What draws me to [COMPANY] is [SPECIFIC REASON — a launch,
a customer, a technical decision]. I would be bringing
[SKILL 1] and [SKILL 2], which is exactly what the
posting asks for in the first two bullets.

[CONTACT] is happy to be quoted as a reference.

Twenty minutes next week would be enough for me to show
you how I would start on [FIRST TASK]. [DAY] or [DAY]
suit me.

Best regards,
[YOUR NAME]</div>
    <div class="note" style="margin-top:4mm;flex:0 0 auto">
      <b>Use when:</b> someone introduced you, or you spoke to the team at an event.
      Always name the person in line one — that is the reason the letter gets opened.
    </div>
  </div>
  <div class="form">
    <h4>C · The cold, no-vacancy letter</h4>
    <div class="code">Dear [NAME],

I will keep this short. I noticed [COMPANY] [SPECIFIC
OBSERVATION — a hiring spree, a new market, a review
complaint pattern, a shipped feature].

I have spent the last [N] years doing exactly that kind of
work: at [EMPLOYER] I [RESULT + NUMBER], and before that
[SECOND PROOF]. [OPTIONAL: LINK TO ONE PIECE OF WORK].

I am not sending a generic CV — the attached one is written
for [THIS PROBLEM], because that is what I would be doing
in the first 90 days.

If it is useful, I would take 15 minutes to show you the
three things I would change first. If it is not, a one-line
no is completely fine and I will not follow up again.

[YOUR NAME] · [PHONE] · [LINK]</div>
    <div class="note" style="margin-top:4mm;flex:0 0 auto">
      <b>Use when:</b> no vacancy is advertised. The one-line-no offer is deliberate —
      it removes the cost of replying and roughly doubles responses.
    </div>
  </div>
</div>
""", "Cover letters", "11")

# ------------------------------------------------------------------ BULLET BANK
BANK = [
    ("Revenue & growth", [
        "Grew [METRIC] from [X] to [Y] in [TIMEFRAME], contributing [$] in [NEW REVENUE / PIPELINE].",
        "Reopened [LOST SEGMENT / REGION], closing [$] in the first [N] months against a [$] target.",
        "Moved [CONVERSION] from [X]% to [Y]% by [ONE SPECIFIC CHANGE] — worth [$] annually.",
        "Cut [COST] by [X]% ([$/unit]) while [QUALITY METRIC] stayed flat.",
        "Took [PRODUCT] from [0/launch] to [USERS / ARR] in [TIMEFRAME].",
        "Recovered [$] of [CHURNED / DORMANT] revenue with a [N]-step win-back sequence.",
    ]),
    ("Ops & efficiency", [
        "Cut [PROCESS] cycle time from [X] to [Y] hours by [WHAT YOU CHANGED].",
        "Automated [TASK], removing [N] hours of manual work per week for a team of [N].",
        "Reduced [ERROR RATE / DEFECTS] from [X]% to [Y]% with [CHECK / TEST / REVIEW STEP].",
        "Consolidated [N] vendors into [M], releasing [$] per year with no service loss.",
        "Cut [WASTE / DOWNTIME / REWORK] by [X]% across [N] sites in [TIMEFRAME].",
        "Built the [SOP / RUNBOOK / PLAYBOOK] still used by [N] people [N] years later.",
    ]),
    ("People & leadership", [
        "Managed a team of [N] ([N] direct reports) across [LOCATIONS], with [N]% retention.",
        "Hired and onboarded [N] in [TIMEFRAME], reaching full productivity in [N] weeks instead of [N].",
        "Ran [N] [WORKSHOPS / TRAINING SESSIONS] for [N] staff; [MEASURABLE OUTCOME].",
        "Led a [N]-person cross-functional squad through [PROJECT], shipped [N] weeks early.",
        "Introduced [OKRs / 1:1s / RETROS] that lifted [ENGAGEMENT / VELOCITY] score from [X] to [Y].",
        "Moted [N] team members into senior roles within [TIMEFRAME].",
    ]),
    ("Product & engineering", [
        "Shipped [FEATURE] to [N] users; [KEY METRIC] moved [X]% → [Y]% in [TIMEFRAME].",
        "Cut p95 [LATENCY / LOAD TIME] from [X]ms to [Y]ms by [TECHNICAL CHANGE].",
        "Raised test coverage from [X]% to [Y]%, cutting production incidents by [Z]%.",
        "Migrated [SYSTEM] to [TARGET] with [N] minutes of downtime across [N] terabytes.",
        "Designed [SCHEMA / ARCHITECTURE] handling [N] events/day at [COST].",
        "Killed [LEGACY SYSTEM / FEATURE], saving [$] and [N] engineer-hours per month.",
    ]),
    ("Marketing & content", [
        "Grew [CHANNEL] from [X] to [Y] ([Z]%) in [TIMEFRAME] with zero paid spend.",
        "Produced [N] [ASSETS / POSTS / VIDEOS] per month; [ENGAGEMENT] up [Z]%.",
        "Cut cost per lead from [$] to [$] by [ACTION] while volume rose [Z]%.",
        "Launched [CAMPAIGN] reaching [N] people and driving [$] in attributed revenue.",
        "Rewrote [PAGES / SEQUENCES]; [CONVERSION] improved [Z]% ([N] tests, [CONFIDENCE]).",
        "Built the [CONTENT SYSTEM / CALENDAR] that let [N] writers publish [N]/week without edits piling up.",
    ]),
    ("Sales & success", [
        "Closed [$] against a [$] quota ([Z]%) across [N] accounts in [TIMEFRAME].",
        "Expanded existing accounts by [$] ([Z]% growth) through [ACTION].",
        "Cut [SALES CYCLE] from [X] to [Y] days by [CHANGE TO PROCESS].",
        "Lifted [RETENTION / NRR] from [X]% to [Y]% by [INTERVENTION].",
        "Sourced [N] qualified opportunities per month via [CHANNEL], [$] in pipeline.",
        "Turned [N] at-risk accounts into [M] renewals worth [$] in [TIMEFRAME].",
    ]),
    ("Finance & admin", [
        "Managed a [$] budget with [VARIANCE]% variance across [N] cost centres.",
        "Closed the books [X] days faster by [AUTOMATION / REORGANISATION].",
        "Recovered [$] in [OVERBILLING / LEAKAGE / REBATES] found during [AUDIT / REVIEW].",
        "Cut [DSO] from [X] to [Y] days, freeing [$] of working capital.",
        "Built the [FORECAST / MODEL] leadership still uses for [DECISION].",
        "Passed [AUDIT / CERTIFICATION] with zero material findings for [N] consecutive years.",
    ]),
]

bank_rows = "".join(
    f"<tr><td>{grp}</td><td>{'<br>'.join('&ldquo;' + b + '&rdquo;' for b in items)}</td></tr>"
    for grp, items in BANK)
page("Bullet bank", "60 achievement formulas", f"""
<div style="font-size:10px;color:#5A6272;margin-bottom:3.5mm">
Replace every <b>[BRACKET]</b>. If you cannot fill a bracket honestly, delete that formula —
a guessed number is worse than no number, and interviewers dig into exactly the figures you
put on the page. Six bullets of substance beat fifteen duties.
</div>
<table class="t">
  <tr><th style="width:34mm">AREA</th><th>FORMULAS — VERB + WHAT CHANGED + BY HOW MUCH + BY WHEN</th></tr>
  {bank_rows}
</table>
<div class="note" style="margin-top:3.5mm">
<b>No numbers at all?</b> You still have them: frequency (per week), count (N accounts,
N people, N sites), range (top 3 of 40 reps), time saved (hours), or comparison to target.
"There were 40 reps and I placed 3rd" is a metric.
</div>
""", "Bullet bank", "12")

# ------------------------------------------------------------------ POWER VERBS
VERBS = [
    ("Achieved", "accelerated · attained · completed · delivered · exceeded · outperformed · surpassed · won"),
    ("Built", "architected · automated · created · designed · established · founded · launched · structured"),
    ("Changed", "adapted · converted · modernised · overhauled · pivoted · reengineered · restructured · transformed"),
    ("Cut", "consolidated · decreased · eliminated · optimised · reduced · rationalised · streamlined · trimmed"),
    ("Earned", "captured · closed · converted · generated · grew · maximised · produced · renewed"),
    ("Found", "analysed · audited · diagnosed · evaluated · forecast · identified · investigated · measured"),
    ("Fixed", "cleared · corrected · recovered · resolved · restored · reversed · salvaged · stabilised"),
    ("Led", "coached · coordinated · directed · mentored · mobilised · oversaw · supervised · trained"),
    ("Managed", "administered · allocated · controlled · maintained · oversaw · planned · prioritised · scheduled"),
    ("Persuaded", "advocated · campaigned · influenced · lobbied · negotiated · presented · sold · united"),
    ("Improved", "boosted · enhanced · expanded · improved · refined · strengthened · upgraded · refined"),
    ("Saved", "conserved · cut · freed · preserved · reduced · released · spared · unlocked"),
]
verb_rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in VERBS)
page("Power verbs", "120 words, by intent", f"""
<div style="font-size:10px;color:#5A6272;margin-bottom:3.5mm">
"Responsible for", "worked on", "helped with" and "duties included" are the four phrases
that make a resume disappear. Start every bullet with one of these instead — pick the column
that matches what actually happened.
</div>
<table class="t teal">
  <tr><th style="width:34mm">START WITH</th><th>OR REACH FOR</th></tr>
  {verb_rows}
</table>
<table class="t" style="margin-top:5mm">
  <tr><th style="width:66mm">THIS MAKES A RESUME DISAPPEAR</th><th>WRITE THIS INSTEAD</th></tr>
  <tr><td>Responsible for managing the…</td><td>Managed a team of [N]; ran [PROCESS] covering [SCOPE]</td></tr>
  <tr><td>Worked on / helped with…</td><td>Built · launched · rewrote · negotiated · recovered</td></tr>
  <tr><td>Duties included…</td><td>Owned [THING] end to end, from [START] to [END]</td></tr>
  <tr><td>Involved in a number of…</td><td>Delivered [N] [PROJECTS] in [TIMEFRAME]</td></tr>
  <tr><td>Successfully…</td><td>Delete it. The number already proves success.</td></tr>
  <tr><td>Various / several / a range of</td><td>The actual count: 6, 14, 3 markets, 2 regions</td></tr>
  <tr><td>Team player, hard worker, self-starter</td><td>Delete, or replace with evidence: "Mentored 4 juniors"</td></tr>
  <tr><td>Utilised / leveraged</td><td>Used. Plain verbs read as confident, not padded.</td></tr>
  <tr><td>Thought outside the box</td><td>Say what you did differently and what it changed</td></tr>
</table>
<div class="cols2" style="margin-top:4mm">
  <div class="note"><b>Present tense for your current job, past tense for everything else.</b>
  "Led" for 2023, "lead" for today. No "-ing" endings — "Led a team" beats "Leading a team"
  because it says the thing already happened.</div>
  <div class="note"><b>One verb per bullet, no repeats on a page.</b> If you used "managed"
  three times, two of them should have been "ran", "owned", "oversaw" or "coordinated" —
  or two of those bullets should be one bullet.</div>
</div>
""", "Power verbs", "13")

# ------------------------------------------------------------------ LINKEDIN
page("LinkedIn rewrite", "Headline · About · Experience", f"""
<div class="cols3">
  <div class="form">
    <h4>Headline — 220 characters</h4>
    <div class="lbl">Formula</div>
    <div class="code"><i>[WHAT YOU ARE]</i> at <i>[COMPANY]</i> |
<i>[SKILL]</i> · <i>[SKILL]</i> |
<i>[ONE RESULT WITH A NUMBER]</i></div>
    <div class="lbl">Examples</div>
    <div class="code">Marketing Manager · Lifecycle &amp; SEO |
Grew 2 SaaS newsletters past 20k subscribers

Backend Engineer (Go, Kafka) |
Cut p95 API latency 840ms → 190ms

Product Designer, fintech | Design systems
&amp; checkout optimisation | +$1.1M recovered</div>
    <div class="note" style="margin-top:3mm;flex:0 0 auto">
      Your headline is the only line that appears in search, comments and messages.
      Writing "Unemployed" or "Looking for opportunities" hides you from recruiters
      who search by job title.</div>
  </div>
  <div class="form">
    <h4>About — 3 short paragraphs</h4>
    <div class="lbl">Structure</div>
    <div class="code"><i>P1 — who + proof (3 lines).</i>
The work I do, for whom, and the single
strongest number you can attribute to it.

<i>P2 — how you work (3 lines).</i>
The method: research → build → measure.
Name the tools. Say what you own.

<i>P3 — what you want (2 lines).</i>
The kind of problem, team and stage you
are looking for next. End with an invite:
"Happy to talk about [TOPIC]."

<i>Then 5 lines of keywords, one per line.</i>
They read badly and search perfectly.</div>
    <div class="note" style="margin-top:3mm;flex:0 0 auto">
      First person, no "I am a results-driven…". Write it the way you would explain your
      job to a smart friend in a queue.</div>
  </div>
  <div class="form">
    <h4>Experience — bullets that read</h4>
    <div class="lbl">Rule</div>
    <div class="code">Same bullet as the resume —
but shorten to 2 lines each, and put the
number at the FRONT when it is strong:

<b>61%</b> more qualified demos YoY, spend flat.
<b>$1.1M</b> recovered by a 6-step → 3-step
checkout redesign.
<b>41%</b> abandonment, down from 63%.</div>
    <div class="lbl">Also fill in</div>
    <ul class="t tight">
      <li>Every skills section — recruiters filter on these, not on your prose.</li>
      <li>Custom URL (linkedin.com/in/yourname).</li>
      <li>Featured: one link, one PDF, one post. Empty Featured looks abandoned.</li>
      <li>Open to — "Open to work" visible only to recruiters if you choose that setting.</li>
    </ul>
  </div>
</div>
""", "LinkedIn rewrite", "14")

# ------------------------------------------------------------------ INTERVIEW
INTERVIEW = [
    ("Tell me about yourself", "Present → past → future, 90 seconds, no biography.",
     "I'm a [ROLE] at [COMPANY], where I [BIGGEST CURRENT RESULT]. Before that I [RELEVANT
     PAST ROLE] at [COMPANY], where I [SECOND PROOF]. What I'm looking for now is [WHAT THE
     JOB OFFERS] — which is why this role caught my attention."),
    ("Why this company?", "Two facts only, both from your research.",
     "Two things. First, [SPECIFIC PRODUCT/DECISION/ANNOUNCEMENT] — I read/watched [SOURCE]
     and it told me you're [INSIGHT]. Second, [TEAM/PROBLEM] is exactly the kind of work I
     did at [EXAMPLE], and I'd bring that pattern across."),
    ("Why are you leaving?", "Forward-facing, never bitter.",
     "I've learned a lot at [CURRENT], especially [GOOD THING]. The honest reason I'm looking
     is that the work is moving toward [DIRECTION] and I want [MORE/OTHER], which is what
     this role is built around."),
    ("Biggest weakness?", "Real, small, and already being managed.",
     "[REAL WEAKNESS, NOT 'PERFECTIONISM']. Early on it showed up as [SPECIFIC EXAMPLE].
     What I do now is [COUNTERMEASURE], and the result is [WHAT IMPROVED]."),
    ("Tell me about a failure", "STAR, and spend most of the answer on the fix.",
     "Situation: [CONTEXT IN ONE LINE]. Task: [WHAT WAS ON ME]. Action: [WHAT I DID —
     including the mistake]. Result: [WHAT IT COST] and [WHAT CHANGED AFTERWARDS]."),
    ("Where do you see yourself in 5 years?", "Anchor it to the role, not a title ladder.",
     "Still doing [THIS KIND OF WORK] really well — ideally at a level where I [BIGGER
     SCOPE]. Titles follow that; what I care about is [REASON RELEVANT TO THEM]."),
    ("What's your salary expectation?", "Give a researched range, then hand the question back.",
     "Based on the market for [ROLE] in [LOCATION] and what I'd be bringing — [ONE LINE OF
     PROOF] — I'm looking at [LOW] to [HIGH]. But I'd rather understand the full scope and
     the band you've set before locking a number."),
    ("Do you have any questions?", "Always three, at least one about the first 90 days.",
     "1) What would make the first 90 days obviously successful? 2) What's the biggest
     thing the person in this role would inherit that isn't in the job ad? 3) How does the
     team decide what not to work on?"),
]
iv_rows = "".join(
    f"<tr><td>{q}<br><span style='font-weight:400;color:#5A6272;font-size:8.5px'>{g}</span></td>"
    f"<td>{a}</td></tr>" for q, g, a in INTERVIEW)
page("Interview answers", "8 questions that always come", f"""
<table class="t">
  <tr><th style="width:74mm">QUESTION + STRATEGY</th><th>YOUR SCAFFOLD — FILL THE BRACKETS</th></tr>
  {iv_rows}
</table>
<div class="note" style="margin-top:3.5mm">
<b>Answer in 90 seconds, then stop talking.</b> The commonest self-inflicted rejection is
filling a silence with more examples. Say the answer, then let them ask for the detail —
the second question is where the interview is actually won.
</div>
""", "Interview", "15")

# ------------------------------------------------------------------ FOLLOW UP + SALARY
page("Follow-up & salary scripts", "Emails that get replies", f"""
<div class="cols2">
  <div class="form">
    <h4>Thank-you note — within 24 hours</h4>
    <div class="code">Subject: <b>Re: [JOB TITLE] — thanks for today</b>

Hi [NAME],

Thank you for the time today. What stayed
with me was [SPECIFIC THING THEY SAID — one
sentence showing you were listening].

You asked how I'd handle [THEIR QUESTION].
The short version: [ONE PARAGRAPH, WITH THE
EXAMPLE YOU WISH YOU'D GIVEN].

I'm more interested than I was before we
spoke. If it's useful, I can share [RELEVANT
ARTIFACT] — happy to send it over.

Best,
[YOUR NAME]</div>
    <div class="lbl">Chasing — day 5, day 10, final</div>
    <div class="code">Day 5: <i>"Hi [NAME], no rush at all — checking
in on timing for [ROLE]. Anything I can
clarify in the meantime?"</i>

Day 10: <i>"Hi [NAME], still very interested.
Since we spoke, [ONE NEW RELEVANT THING].
Happy to work to whatever timeline suits."</i>

Final: <i>"Thanks for your time on this. If the
role is filled I'd be grateful for one line of
feedback — and please keep me in mind for
[WHAT COMES NEXT]."</i></div>
  </div>
  <div class="form">
    <h4>Salary negotiation — the sequence</h4>
    <table class="t teal">
      <tr><th>STEP</th><th>WHAT YOU SAY</th></tr>
      <tr><td>1 · They ask first</td><td>"Happy to share — what's the band you've set for
        this level?" Get their number before yours.</td></tr>
      <tr><td>2 · You must give a range</td><td>Research floor × 1.15 to floor × 1.35.
        "For this scope and location I'm seeing [LOW]–[HIGH]."</td></tr>
      <tr><td>3 · They lowball</td><td>"I appreciate that. Given [PROOF OF SCOPE], I'd be
        expecting closer to [NUMBER]. What flexibility is there?"</td></tr>
      <tr><td>4 · Verbal offer</td><td>"Thank you — could you send it in writing? I'd like
        to look at it properly before responding."</td></tr>
      <tr><td>5 · You want more</td><td>"I'm excited about this. To say yes today I'd need
        [X] — is that possible?" One ask, stated once, then silence.</td></tr>
      <tr><td>6 · Not money</td><td>Sign-on bonus · earlier review date · extra leave ·
        remote days · title · learning budget · relocation · start date.</td></tr>
      <tr><td>7 · The pause</td><td>Never fill it. Whoever speaks first after "is that
        possible?" usually concedes.</td></tr>
    </table>
    <div class="note" style="margin-top:3mm;flex:1 1 auto">
      <b>Never accept in the call.</b> "I'm very interested — send it over and I'll confirm
      tomorrow" costs you nothing and has never lost anyone an offer that was going to be
      withdrawn. Rehearse that one sentence until it is automatic.
    </div>
  </div>
</div>
""", "Follow-up & salary", "16")

# ------------------------------------------------------------------ LICENCE
page("Terms & licence", "Please read", f"""
<div class="cols2">
  <div class="card">
    <h4>You may</h4>
    <ul class="t">
      <li>Copy any text, formula or layout from this kit into your own applications, as many
      times as you like, forever.</li>
      <li>Print it, annotate it, keep it open in a second window while you write.</li>
      <li>Use the templates for your own job search, career changes and promotions.</li>
    </ul>
    <div class="note" style="margin-top:4mm">
      <b>Digital goods policy:</b> this is an instant-download file, so all sales are final
      and no refunds are issued. If a file will not open, message the seller and it will be
      replaced or the problem fixed.
    </div>
  </div>
  <div class="card">
    <h4>You may not</h4>
    <ul class="t">
      <li>Resell, share or redistribute the PDF — including "free bonus" downloads on your own site.</li>
      <li>Upload it to a shared cloud folder, a forum, or a Telegram channel.</li>
      <li>Turn the kits into a product you sell, in whole or in part.</li>
      <li>Claim the templates as your own design.</li>
    </ul>
    <div class="note" style="margin-top:4mm">
      <b>One honest disclaimer:</b> this kit makes applications stronger; it cannot promise
      interviews. Hiring depends on the market, the role and the people. What it does remove
      is every preventable reason to be filtered out.
    </div>
  </div>
</div>
<div class="card" style="margin-top:5mm;flex:0 0 auto">
  <h4>The five-minute final check before you hit send</h4>
  <ul class="t tight">
    <li>Filename is <b>Firstname-Lastname-Resume.pdf</b> and the cover letter matches it.</li>
    <li>Top third of page one answers: role, strongest number, current title.</li>
    <li>Every keyword from the job description appears somewhere in the document.</li>
    <li>At least six bullets carry a number. No bullet starts with "Responsible for".</li>
    <li>You would be comfortable defending every claim on the page for five minutes.</li>
    <li>You addressed a human by name, and you said what you want in the first two lines.</li>
  </ul>
</div>
""", "Terms & licence", "17")

html_doc = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<title>The Resume &amp; Cover Letter Kit 2026</title>"
            f"<style>{CSS}</style></head><body>" + "\n".join(P) + "</body></html>")

html_path = OUT / "resume_kit_2026.html"
pdf_path = OUT / "Resume_and_Cover_Letter_Kit_2026.pdf"
html_path.write_text(html_doc, encoding="utf-8")

subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", str(html_path)],
               check=True, capture_output=True, timeout=180)

print("pages:", len(P))
print("html :", html_path.stat().st_size, "bytes")
print("pdf  :", pdf_path.stat().st_size, "bytes")
