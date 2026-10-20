import pathlib

base = pathlib.Path(__file__).resolve().parent

PACKS = {
    "ai-video-reels-script-prompts.txt": ["_p1_1", "_p1_2", "_p1_3", "_p1_4", "_p1_5"],
    "cold-outreach-sales-prompt-prompts.txt": ["_p2_1", "_p2_2", "_p2_3", "_p2_4"],
    "job-search-resume-interview-prompts.txt": ["_p3_1", "_p3_2", "_p3_3", "_p3_4"],
}

for out, parts in PACKS.items():
    chunks = []
    for name in parts:
        raw = (base / (name + ".txt")).read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        chunks.append(text.rstrip("\n"))
    merged = "\n\n".join(chunks) + "\n"
    merged = merged.replace("\r\n", "\n").replace("\r", "\n")
    (base / out).write_bytes(merged.encode("utf-8"))
    print(f"{out}: {len(merged.encode('utf-8'))} bytes, {merged.count('### P')} prompts")
