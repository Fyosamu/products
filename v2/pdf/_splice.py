# -*- coding: utf-8 -*-
"""One-shot splice: move INTERVIEW into layouts.py and import it."""
import io

INTERVIEW_BLOCK = '''

INTERVIEW = [
    ("Tell me about yourself",
     "Present to past to future, 90 seconds, no biography.",
     """I am a [ROLE] at [COMPANY], where I [BIGGEST CURRENT RESULT]. Before that I was
[RELEVANT PAST ROLE] at [COMPANY], where I [SECOND PROOF]. What I am looking for now
is [WHAT THE JOB OFFERS] - which is why this role caught my attention."""),
    ("Why this company?",
     "Two facts only, and both from your own research.",
     """Two things. First, [SPECIFIC PRODUCT / DECISION / ANNOUNCEMENT] - I read [SOURCE]
and it told me [INSIGHT]. Second, [TEAM OR PROBLEM] is exactly the kind of work I did
when [EXAMPLE], and I would bring that pattern across."""),
    ("Why are you leaving?",
     "Forward-facing, and never bitter.",
     """I have learned a lot at [CURRENT], especially [GOOD THING]. The honest reason I
am looking is that the work is moving toward [DIRECTION] and I want [MORE OR OTHER],
which is what this role is built around."""),
    ("Biggest weakness?",
     "Something real, small, and already under management.",
     """[REAL WEAKNESS - NOT 'PERFECTIONISM']. Early on it showed up as [SPECIFIC
EXAMPLE]. What I do now is [COUNTERMEASURE], and the result is [WHAT IMPROVED]."""),
    ("Tell me about a failure",
     "STAR format - and spend most of the answer on the fix.",
     """Situation: [CONTEXT IN ONE LINE]. Task: [WHAT WAS ON ME]. Action: [WHAT I DID,
including the mistake]. Result: [WHAT IT COST] and [WHAT CHANGED AFTERWARDS]."""),
    ("Where do you see yourself in five years?",
     "Anchor it to the work, not to a title ladder.",
     """Still doing [THIS KIND OF WORK] really well - ideally at a level where I have
[BIGGER SCOPE]. Titles follow that. What I care about is [REASON RELEVANT TO THEM]."""),
    ("What is your salary expectation?",
     "Give a researched range, then hand the question back.",
     """Based on the market for [ROLE] in [LOCATION] and what I would be bringing -
[ONE LINE OF PROOF] - I am looking at [LOW] to [HIGH]. But I would rather understand
the full scope and the band you have set before locking a number."""),
    ("Do you have any questions?",
     "Always three, and at least one about the first 90 days.",
     """1) What would make the first 90 days obviously successful?
2) What is the biggest thing the person in this role inherits that is not in the job ad?
3) How does the team decide what not to work on?"""),
]
'''

layouts = r"products\v2\pdf\layouts.py"
build = r"products\v2\pdf\build_resume_kit.py"

s = io.open(layouts, encoding="utf-8").read()
if "INTERVIEW = [" not in s:
    io.open(layouts, "w", encoding="utf-8", newline="\n").write(s + INTERVIEW_BLOCK)
    print("layouts.py: INTERVIEW appended")
else:
    print("layouts.py: INTERVIEW already present")

lines = io.open(build, encoding="utf-8").read().split("\n")
assert lines[640].startswith("INTERVIEW = ["), lines[640]
assert lines[671].startswith("iv_rows = "), lines[671]
new = lines[:640] + ["from layouts import INTERVIEW", ""] + lines[671:]
io.open(build, "w", encoding="utf-8", newline="\n").write("\n".join(new))
print("build_resume_kit.py: INTERVIEW block spliced")
