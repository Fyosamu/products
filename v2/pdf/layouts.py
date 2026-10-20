# -*- coding: utf-8 -*-
"""Resume layout data for build_resume_kit.py."""

contact = ('[CITY], [COUNTRY] &nbsp;·&nbsp; [PHONE] &nbsp;·&nbsp; '
           '[EMAIL] &nbsp;·&nbsp; linkedin.com/in/[HANDLE] &nbsp;·&nbsp; [PORTFOLIO IF RELEVANT]')

LAYOUTS = [
    dict(
        n="Layout 1 — Compact single-column", tag="Safest · default choice",
        why=("One column, no graphics, parses perfectly in every applicant tracking system. "
             "Use this when you are applying to a large company, or when you are not sure "
             "which layout to pick. It is not the prettiest — it is the most reliable."),
        name="JORDAN A. MERCER", role="Marketing Manager",
        sections=[
            ("SUMMARY", [
                "Marketing manager with 6 years turning search and email into predictable "
                "pipeline. Grew two B2B SaaS newsletters past 20k subscribers and cut cost "
                "per lead 38% in one year. Comfortable owning budget, agency and roadmap."]),
        ],
        jobs=[
            ("MARKETING MANAGER", "Northwind Software", "2022 — Present",
             ["Own paid search, lifecycle email and the blog for a $14M ARR product; grew "
              "qualified demos 61% YoY while holding spend flat.",
              "Rebuilt the lifecycle sequence (11 emails); trial-to-paid moved 4.2% → 7.9% in two quarters.",
              "Manage two specialists plus a $480k annual budget and a three-agency roster."]),
            ("MARKETING SPECIALIST", "Brightline Analytics", "2020 — 2022",
             ["Ran the webinar programme: 24 events, 5,900 registrants, 310 sourced opportunities.",
              "Cut cost per lead from $84 to $52 by killing three channels and doubling down on one.",
              "Wrote the 40-page demand-gen playbook the sales team now uses as its qualification guide."]),
            ("MARKETING ASSISTANT", "Halberd Media", "2018 — 2020",
             ["Produced 90 SEO articles a year; organic sessions grew 210% over two years.",
              "Ran the weekly newsletter to 18,400 subscribers at a 41% open rate (industry: 21%)."]),
        ],
        side=("EDUCATION", "BSc Marketing, University of Leeds, 2020"),
        skills="SEO · Google Ads · HubSpot · GA4 · Lifecycle email · Copywriting · SQL basics · Budget ownership"),
    dict(
        n="Layout 2 — Modern timeline", tag="Best for 3–10 years' experience",
        why=("Same parser-friendly structure, but the date column is pulled out to the right "
             "so the eye can scan tenure instantly. Use it when your career is steady and you "
             "want the page to feel designed without breaking a single ATS rule."),
        name="PRIYA RAGHUNATHAN", role="Senior Product Designer",
        sections=[
            ("PROFILE", [
                "Product designer, 7 years, fintech and marketplace. Ships research-to-release "
                "on small teams. Redesigned a checkout that recovered $1.1M in annual revenue."]),
        ],
        jobs=[
            ("SENIOR PRODUCT DESIGNER", "Kestrel Pay", "2023 — Present",
             ["Led the redesign of a 6-step checkout to 3 steps; abandonment 63% → 41%, roughly $1.1M/yr recovered.",
              "Built and documented the design system (84 components) now used by 5 squads.",
              "Runs the weekly critique and mentors two mid-level designers."]),
            ("PRODUCT DESIGNER", "Marketplace Co", "2020 — 2023",
             ["Shipped seller onboarding; activation in the first session rose 27% (n = 41k).",
              "Ran 60+ usability sessions and turned the findings into a quarterly experiment backlog.",
              "Cut the design-to-dev handoff from 9 days to 3 by rewriting the spec template."]),
            ("UX DESIGNER", "Orbit Studio", "2018 — 2020",
             ["Delivered 22 client projects across retail and health; 19 shipped without a redesign round.",
              "Introduced the studio's first accessibility audit — now standard on every engagement."]),
        ],
        side=("EDUCATION", "BDes Interaction Design, NID, 2018"),
        skills="Figma · Design systems · Usability testing · Prototyping · Accessibility (WCAG 2.2) · HTML/CSS literacy"),
    dict(
        n="Layout 3 — Skills-first (career changer)", tag="For switching industries",
        why=("When the job titles on your history do not match the job you want, lead with the "
             "skills that do transfer. The experience section still follows — it simply stops "
             "being the first thing that gets read."),
        name="DANIEL OKONKWO", role="Retail operations → Data analyst",
        sections=[("CORE SKILLS", None), ("RELEVANT PROJECTS", None)],
        jobs=[
            ("SHIFT MANAGER", "Halcyon Grocery Group", "2019 — Present",
             ["Built the weekly sales tracker in a spreadsheet the district now uses across 14 stores.",
              "Cut wastage 19% by re-forecasting produce orders from my own 8-week demand model.",
              "Trained 22 staff; halved till-error rate in the first quarter after training."]),
            ("DATA & REPORTING TEMP", "Lagos Trade Bureau", "Jun — Sep 2017",
             ["Rebuilt a 3,000-row import sheet with validation rules; error rate fell 70%.",
              "Produced the weekly imports-versus-exports brief the director took to meetings."]),
        ],
        side=("EDUCATION", "BSc Economics, University of Lagos, 2017 · Google Data Analytics Certificate, 2025"),
        skills="SQL (joins, CTEs, window functions) · Python (pandas) · Power BI · Excel (Power Query) · A/B testing · Statistics",
        skip_skills=True, chips=True,
        projects=[("Demand forecasting model", "Python + pandas on 8 weeks of store data; MAPE 6.4%."),
                  ("Wastage dashboard", "Power BI, refreshed daily; now standard across 14 stores."),
                  ("Checkout queue simulation", "Discrete-event model that justified a second till on Saturdays.")]),
    dict(
        n="Layout 4 — Technical / engineering", tag="Projects beat job titles",
        why=("Engineers get screened on stack and shipped work. Put the stack in a scannable "
             "strip at the top, then let impact carry the page. Keep education to one line."),
        name="MIRA TANAKA", role="Backend Engineer",
        sections=[("STACK", None)],
        jobs=[
            ("BACKEND ENGINEER", "Loomstack", "2022 — Present",
             ["Cut p95 API latency 840ms → 190ms by moving session reads to Redis and fixing three N+1 queries.",
              "Designed the idempotent payment webhook that stopped duplicate charges (0 in 14 months).",
              "Own the on-call runbook; mean time to recovery down from 47 to 12 minutes."]),
            ("JUNIOR DEVELOPER", "Cartwheel Labs", "2020 — 2022",
             ["Wrote the CSV import service still handling 40k files a day.",
              "Raised backend test coverage 34% → 81% and wired it into CI.",
              "Owned two production services on a five-person on-call rotation."]),
            ("SOFTWARE INTERN (SUMMER)", "Kiwi Systems", "2019",
             ["Wrote the nightly reconciliation job that replaced a 90-minute manual morning routine.",
              "Presented the team's first written latency budget to the platform group."]),
        ],
        side=("EDUCATION", "BSc Computer Science, University of Auckland, 2020"),
        stack="Go · Python · PostgreSQL · Redis · Kafka · Docker · Kubernetes",
        skills="AWS (ECS, RDS, S3) · Terraform · OpenTelemetry · CI/CD · Distributed systems · Code review · On-call ownership",
        chips=True),
    dict(
        n="Layout 5 — Graduate / entry level", tag="Under 2 years of experience",
        why=("You have almost no job history, so lead with education, internship, projects and "
             "anything measurable. Three bullets per item is plenty — padding reads as "
             "inexperience to anyone who has read a hundred graduate CVs."),
        name="TOMÁS HERRERA", role="Junior Financial Analyst — graduate",
        sections=[("EDUCATION", None), ("INTERNSHIP", None), ("PROJECTS", None),
                  ("ACTIVITIES", None)],
        jobs=[],
        side=None, grad=True,
        skills="Excel (INDEX/MATCH, pivots, Power Query) · Financial modelling · Valuation · Power BI · Python basics"),
    dict(
        n="Layout 6 — Executive / senior leader", tag="10+ years · P&L · board-facing",
        why=("Still one page, but the top third is a leadership summary carrying scope: "
             "revenue, headcount, geographies. Chronology below is compressed to three lines "
             "per role — nobody hiring a director needs your 2009 bullet points."),
        name="HELENA VOSS", role="Chief Operating Officer",
        sections=[("LEADERSHIP SUMMARY", [
            "Operator who takes multi-country businesses from marginal to compounding. Currently "
            "running a 340-person, 4-country group at 24% EBITDA, up from 11% in three years. "
            "Two acquisitions integrated, zero regretted attrition in year one."])],
        jobs=[
            ("CHIEF OPERATING OFFICER", "Ridgeline Group", "2021 — Present",
             ["Took a 340-person, 4-country operation from 11% to 24% EBITDA in three years.",
              "Integrated two acquisitions (180 staff) with zero regretted attrition in year one."]),
            ("VP OPERATIONS", "Ridgeline Group", "2017 — 2021",
             ["Built the ops function from 6 to 120 people and introduced quarterly OKRs across all teams.",
              "Renegotiated the top 12 suppliers, releasing $4.2M of annualised cost."]),
            ("GENERAL MANAGER", "Voss &amp; Partners", "2013 — 2017",
             ["Ran a 60-person regional business through a turnaround from -4% to +9% margin.",
              "Opened two new sites, both profitable inside 11 months."]),
        ],
        side=("EDUCATION", "MBA, INSEAD, 2012 · BEng, TU Delft, 2006"),
        skills="P&L ownership · M&A integration · Supply chain · Multi-site operations · Board reporting · Change management",
        chips=True),
]
