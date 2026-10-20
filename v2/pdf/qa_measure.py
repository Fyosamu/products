# -*- coding: utf-8 -*-
"""Measure each .page's real content height (headless Chrome + --dump-dom)."""
import pathlib, re, subprocess, html as htmllib

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
here = pathlib.Path(__file__).parent
import sys as _sys
STEM = _sys.argv[1] if len(_sys.argv) > 1 else "planner_2026"
src = here / (STEM + ".html")

MEASURE = """
<script>
window.addEventListener('load', function(){
  var pages = document.querySelectorAll('.page');
  var out = [];
  for (var i=0;i<pages.length;i++){
    pages[i].style.height='auto';
    pages[i].style.overflow='visible';
    out.push('PAGE '+(i+1)+' height=' + Math.round(pages[i].getBoundingClientRect().height*10/37.795275591) + 'mm');
  }
  var d=document.createElement('pre'); d.id='MEASUREOUT'; d.textContent='MEASURE_START\\n'+out.join('\\n')+'\\nMEASURE_END';
  document.body.insertBefore(d, document.body.firstChild);
});
</script>
"""
h = src.read_text(encoding="utf-8")
h = h.replace("</body>", MEASURE + "</body>", 1)
qa = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode") / ("measure_" + STEM + ".html")
qa.write_text(h, encoding="utf-8")

p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--virtual-time-budget=4000", "--dump-dom", qa.as_uri()],
                   capture_output=True, text=True, timeout=300)
dom = p.stdout
m = re.search(r"MEASURE_START(.*?)MEASURE_END", dom, re.S)
if not m:
    print("no output"); print(p.stderr[-1500:]); raise SystemExit(1)

LIMIT = 286  # 297 total - ~11mm reserved for the absolutely-positioned footer
bad = 0
for line in m.group(1).strip().splitlines():
    n = int(re.search(r"PAGE (\d+)", line).group(1))
    mm = int(re.search(r"height=(\d+)mm", line).group(1))
    flag = ""
    if mm > LIMIT:
        flag = "   <-- OVERFLOWS by %dmm" % (mm - LIMIT)
        bad += 1
    print(f"{line}{flag}")
print(f"\npages over limit: {bad}")
