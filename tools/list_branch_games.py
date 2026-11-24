import subprocess

REPO_DIR = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game"

r = subprocess.run(["git", "ls-remote", "--heads", "origin"], cwd=REPO_DIR, capture_output=True, text=True)
branches = [l.split("\t")[1].replace("refs/heads/", "").strip() for l in r.stdout.splitlines()]

print(f"Total remote branches: {len(branches)}")
for b in sorted(branches):
    if b.startswith("codex/"):
        continue
    subprocess.run(["git", "fetch", "origin", b], cwd=REPO_DIR, capture_output=True)
    r3 = subprocess.run(["git", "show", "FETCH_HEAD:pubspec.yaml"], cwd=REPO_DIR, capture_output=True, text=True)
    name = "UNKNOWN"
    desc = ""
    for line in r3.stdout.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip()
    print(f"Branch: {b:28} | Name: {name:20} | {desc[:40]}")