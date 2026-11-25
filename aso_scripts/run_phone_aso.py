import argparse
import os
import shutil
import subprocess
import sys
import time


def find_flutter():
    env_root = os.environ.get("FLUTTER_ROOT", "").strip()
    candidates = []
    if env_root:
        candidates.extend([
            os.path.join(env_root, "bin", "flutter.bat"),
            os.path.join(env_root, "bin", "flutter"),
        ])
    for name in ("flutter.bat", "flutter"):
        w = shutil.which(name)
        if w:
            candidates.append(w)
    user_home = os.path.expanduser("~")
    candidates.extend([
        r"C:\flutter\bin\flutter.bat",
        r"C:\src\flutter\bin\flutter.bat",
        r"D:\flutter\bin\flutter.bat",
        os.path.join(user_home, "flutter", "bin", "flutter.bat"),
        os.path.join(user_home, "fvm", "default", "bin", "flutter.bat"),
    ])
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError("Could not locate flutter executable. Ensure Flutter is in PATH or set FLUTTER_ROOT.")


def find_adb():
    w = shutil.which("adb.exe") or shutil.which("adb")
    if w:
        return w
    candidates = []
    for var in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
        val = os.environ.get(var, "").strip()
        if val:
            candidates.extend([
                os.path.join(val, "platform-tools", "adb.exe"),
                os.path.join(val, "platform-tools", "adb"),
            ])
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        candidates.append(os.path.join(local, "Android", "Sdk", "platform-tools", "adb.exe"))
    user_home = os.path.expanduser("~")
    candidates.extend([
        os.path.join(user_home, "AppData", "Local", "Android", "Sdk", "platform-tools", "adb.exe"),
        os.path.join(user_home, "Android", "Sdk", "platform-tools", "adb"),
    ])
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError("Could not locate adb. Ensure Android platform-tools is in PATH or set ANDROID_HOME.")


def resolve_device(adb_bin, requested):
    if requested and requested.lower() != "auto":
        return requested
    out = subprocess.check_output([adb_bin, "devices"], text=True, stderr=subprocess.STDOUT)
    devs = []
    for line in out.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devs.append(parts[0])
    if not devs:
        raise RuntimeError(f"No online ADB devices found.\nOutput:\n{out}")
    if "ZD222PJ69H" in devs:
        return "ZD222PJ69H"
    return devs[0]


def run_adb(adb_bin, device, args):
    return subprocess.run([adb_bin, "-s", device] + args, capture_output=True, text=True)


def main():
    p = argparse.ArgumentParser(description="Run Flutter integration_test live on physical Android device and capture screenshots + screenrecord.")
    p.add_argument("--game-dir", required=True)
    p.add_argument("--raw-dir", required=True)
    p.add_argument("--video-out", required=True)
    p.add_argument("--device", default="auto", help="ADB serial (or 'auto' to pick first online phone)")
    p.add_argument("--test-path", default=os.path.join("integration_test", "_phone_aso_test.dart"))
    p.add_argument("--log-file", default="")
    p.add_argument("--bit-rate", default="20000000")
    p.add_argument("--time-limit", default="55")
    args = p.parse_args()

    adb_bin = find_adb()
    flutter_bin = find_flutter()
    device = resolve_device(adb_bin, args.device)
    print(f"[ENV] flutter={flutter_bin} | adb={adb_bin} | device={device}", flush=True)

    os.makedirs(args.raw_dir, exist_ok=True)
    vid_parent = os.path.dirname(os.path.abspath(args.video_out))
    os.makedirs(vid_parent, exist_ok=True)

    run_adb(adb_bin, device, ["shell", "input", "keyevent", "224"])
    run_adb(adb_bin, device, ["shell", "svc", "power", "stayon", "usb"])
    run_adb(adb_bin, device, ["shell", "rm", "-f", "/sdcard/aso_phone_rec.mp4"])

    subprocess.run([flutter_bin, "pub", "get", "--offline"], cwd=args.game_dir, capture_output=True)

    log_lines = []
    rec_proc = {"p": None}

    fl_proc = subprocess.Popen(
        [flutter_bin, "test", args.test_path, "-d", device, "--no-pub"],
        cwd=args.game_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    for raw_line in iter(fl_proc.stdout.readline, ""):
        s = raw_line.rstrip()
        log_lines.append(s)
        if "ASO_SNAP:" in s:
            fname = s.split("ASO_SNAP:", 1)[1].strip().split()[0]
            dst = os.path.join(args.raw_dir, fname)
            time.sleep(0.15)
            data = subprocess.run([adb_bin, "-s", device, "exec-out", "screencap", "-p"], capture_output=True).stdout
            if len(data) > 5000:
                with open(dst, "wb") as f:
                    f.write(data)
            print(f"[SNAP] {fname} ({len(data)} bytes)", flush=True)
        elif "ASO_REC_START" in s and rec_proc["p"] is None:
            print("[REC] Starting screenrecord on phone...", flush=True)
            rec_proc["p"] = subprocess.Popen(
                [adb_bin, "-s", device, "shell", "screenrecord", "--bit-rate", str(args.bit_rate), "--time-limit", str(args.time_limit), "/sdcard/aso_phone_rec.mp4"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif "ASO_REC_STOP" in s and rec_proc["p"] is not None:
            print("[REC] Stopping screenrecord cleanly...", flush=True)
            run_adb(adb_bin, device, ["shell", "pkill -2 screenrecord || killall -2 screenrecord || true"])
            time.sleep(2.0)
            try:
                rec_proc["p"].wait(timeout=5)
            except Exception:
                pass
            rec_proc["p"] = None
        elif any(k in s for k in ("+0", "+1", "-1", "All tests passed", "Some tests failed", "Error", "FAILURE", "Exception", "ASO_ALL_DONE")):
            print(s, flush=True)

    ec = fl_proc.wait()
    if rec_proc["p"] is not None:
        run_adb(adb_bin, device, ["shell", "pkill -2 screenrecord || killall -2 screenrecord || true"])
        time.sleep(2.0)

    ls_res = run_adb(adb_bin, device, ["shell", "ls -l /sdcard/aso_phone_rec.mp4"])
    if "aso_phone_rec.mp4" in ls_res.stdout:
        run_adb(adb_bin, device, ["pull", "/sdcard/aso_phone_rec.mp4", args.video_out])
        run_adb(adb_bin, device, ["shell", "rm", "-f", "/sdcard/aso_phone_rec.mp4"])
        if os.path.exists(args.video_out):
            print(f"[VIDEO] Saved {args.video_out} ({os.path.getsize(args.video_out)} bytes)", flush=True)

    run_adb(adb_bin, device, ["shell", "svc", "power", "stayon", "false"])
    if args.log_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.log_file)), exist_ok=True)
        with open(args.log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
    print(f"=== EXIT CODE: {ec} ===", flush=True)
    sys.exit(ec)


if __name__ == "__main__":
    main()
