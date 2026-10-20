import re
import sys

sys.path.insert(0, r"C:\Users\USER\Documents\Default Project\products\v2")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from _sd_session import fetch  # noqa: E402

st, page, _, _ = fetch("/dashboard/products", accept="text/html")
print("status", st, "len", len(page) if isinstance(page, str) else "-")
print("live:", page.count(">live<"), "paused:", page.count(">paused<"), "draft:", page.count(">draft<"))

forms = re.findall(r"<form[^>]*>(.*?)</form>", page, re.S)
print("forms:", len(forms))
for i, f in enumerate(forms):
    fields = re.findall(r"<(?:input|textarea|select)[^>]*>", f)
    names = []
    types = []
    for x in fields:
        m = re.search(r'name="([^"]+)"', x)
        if m:
            names.append(m.group(1))
        m2 = re.search(r'type="([^"]+)"', x)
        if m2:
            types.append(m2.group(1))
        elif "<textarea" in x:
            types.append("textarea")
    print(" form", i, "names:", names[:16])
    print("      types:", types[:14])
    if "file" in types:
        print("      ** HAS FILE UPLOAD **")
