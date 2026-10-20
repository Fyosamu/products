# -*- coding: utf-8 -*-
import io, re, pathlib, subprocess, time

h = io.open(r"products\v2\pdf\resume_kit_2026.html", encoding="utf-8").read()
pages = re.findall(r'<section class="page.*?</section>', h, re.S)
p3 = pages[3]
print("page3 len:", len(p3), "| has ASSISTANT:", "ASSISTANT" in p3)
print("titles found:", re.findall(r'<h2>(.*?)</h2>', p3))

css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
single = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
          "<style>" + css + "</style></head><body>" + p3 + "</body></html>")
out = pathlib.Path(r"C:\Users\USER\AppData\Local\Temp\opencode")
f = out / ("only_%d.html" % int(time.time()))
f.write_text(single, encoding="utf-8")
print("wrote", f.name, len(single), "bytes | ASSISTANT in file:", "ASSISTANT" in single)

png = pathlib.Path(r"C:\Users\USER\Documents\Default Project\products\v2\pdf\_only_layout1.png")
if png.exists():
    png.unlink()
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--window-size=794,1123",
                    "--user-data-dir=" + str(out / ("cdp_%d" % int(time.time()))),
                    f"--screenshot={png}", f.as_uri()],
                   capture_output=True, text=True, timeout=180)
print("rc:", p.returncode, "png:", png.stat().st_size if png.exists() else 0)
