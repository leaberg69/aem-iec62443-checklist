#!/usr/bin/env python3
"""
IEC 62443-4-2 SL2 interactive validator.

Walks the user through the 47 checklist items and emits a Markdown
compliance report with yes/no/N-A answers and rationale.
"""
import argparse
import datetime
from pathlib import Path

CHECKLIST = [
    # (FR, code, statement)
    ("FR1 IAC", "IAC-1.1", "Device has a globally unique identifier read-only by software"),
    ("FR1 IAC", "IAC-1.2", "Identity is exposed via documented interface for supervisor audit"),
    ("FR1 IAC", "IAC-2.1", "Configuration menus require authentication"),
    ("FR1 IAC", "IAC-2.2", "Default credentials forced to change on first commissioning"),
    ("FR1 IAC", "IAC-3.1", "Firmware updates require cryptographic signature verification"),
    ("FR1 IAC", "IAC-3.2", "Signing key rotation is documented and tested"),
    ("FR1 IAC", "IAC-4.1", "At least two roles exist (operator/engineer)"),
    ("FR1 IAC", "IAC-4.2", "Account changes are auditable in device logs"),
    ("FR2 UC", "UC-1.1", "Operator role cannot modify critical settings"),
    ("FR2 UC", "UC-1.2", "Engineer actions logged with timestamp + identity"),
    ("FR2 UC", "UC-2.1", "Wireless interfaces can be disabled"),
    ("FR2 UC", "UC-2.2", "Wireless authentication uses WPA2-Enterprise or stronger"),
    ("FR2 UC", "UC-3.1", "No dynamic code execution from untrusted sources"),
    ("FR2 UC", "UC-3.2", "No exposed interpreter by default"),
    ("FR2 UC", "UC-4.1", "Sessions time out after documented inactivity period"),
    ("FR3 SI", "SI-1.1", "Modbus RTU CRC validation enforced"),
    ("FR3 SI", "SI-1.2", "Out-of-band integrity counter exposed"),
    ("FR3 SI", "SI-2.1", "Firmware signature verified at boot"),
    ("FR3 SI", "SI-2.2", "Anti-rollback protection prevents downgrade"),
    ("FR3 SI", "SI-3.1", "Bootloader in unreachable flash region"),
    ("FR3 SI", "SI-3.2", "Failed validation results in update mode (anti-brick)"),
    ("FR3 SI", "SI-4.1", "Layer 1: Magic word check"),
    ("FR3 SI", "SI-4.2", "Layer 2: Header version check"),
    ("FR3 SI", "SI-4.3", "Layer 3: Header CRC"),
    ("FR3 SI", "SI-4.4", "Layer 4: Hardware ID match"),
    ("FR3 SI", "SI-4.5", "Layer 5: Payload size sanity"),
    ("FR3 SI", "SI-4.6", "Layer 6: Payload CRC"),
    ("FR3 SI", "SI-4.7", "Layer 7: Vector table sanity"),
    ("FR3 SI", "SI-4.8", "Layer 8: Trailer seal"),
    ("FR3 SI", "SI-4.9", "Layer 9: Cryptographic signature"),
    ("FR3 SI", "SI-5.1", "Persistent anti-rollback counter in battery-backed register"),
    ("FR3 SI", "SI-5.2", "Counter saturates at documented maximum"),
    ("FR4 DC", "DC-1.1", "Signing keys in hardware (HSM/Yubikey)"),
    ("FR4 DC", "DC-1.2", "Key rotation exercised at least annually"),
    ("FR4 DC", "DC-2.1", "No PII collected by device"),
    ("FR4 DC", "DC-2.2", "Telemetry does not contain credentials/tokens"),
    ("FR4 DC", "DC-3.1", "No default phone-home behavior"),
    ("FR5 RDF", "RDF-1.1", "Network segments documented"),
    ("FR5 RDF", "RDF-2.1", "Galvanic isolation field/logic side >=5000 VAC rms"),
    ("FR5 RDF", "RDF-2.2", "Opto-isolated digital inputs"),
    ("FR5 RDF", "RDF-3.1", "Config changes authenticated"),
    ("FR5 RDF", "RDF-3.2", "Changes persisted with documented write limits"),
    ("FR6 TRE", "TRE-1.1", "Audit log of security-relevant events"),
    ("FR6 TRE", "TRE-2.1", "Forensic telemetry accessible via Modbus"),
    ("FR6 TRE", "TRE-3.1", "RTC with battery backup or supervisor time sync"),
    ("FR7 RA", "RA-1.1", "Modbus rate-limits malformed requests"),
    ("FR7 RA", "RA-2.1", "Configurable maximum concurrent connections"),
]


def ask(prompt):
    while True:
        a = input(f"{prompt} [y/n/N=N-A/q=quit]: ").strip().lower()
        if a == "q":
            return None
        if a in ("y", "yes"):
            return "Yes"
        if a in ("n", "no"):
            return "No"
        if a in ("na", "n/a", "x"):
            return "N/A"


def run(args):
    print(f"\nIEC 62443-4-2 SL2 Validator")
    print(f"Device: {args.device_name}")
    print(f"Date: {datetime.date.today().isoformat()}\n")
    print(f"Working through {len(CHECKLIST)} items. Press Ctrl-C to abort.\n")
    
    results = []
    for fr, code, statement in CHECKLIST:
        ans = ask(f"[{code}] {statement}")
        if ans is None:
            print("Aborted.")
            return 130
        results.append((fr, code, statement, ans))
        if ans == "No":
            rationale = input("  ↪ Why not? (gap/plan): ").strip()
            results[-1] = (fr, code, statement, ans, rationale)
        elif ans == "N/A":
            rationale = input("  ↪ Why N/A? : ").strip()
            results[-1] = (fr, code, statement, ans, rationale)
    
    out = Path(args.output)
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# IEC 62443-4-2 SL2 Compliance Report\n\n")
        f.write(f"**Device:** {args.device_name}\n")
        f.write(f"**Date:** {datetime.date.today().isoformat()}\n")
        f.write(f"**Validator:** [aem-iec62443-checklist](https://github.com/leaberg69/aem-iec62443-checklist)\n\n")
        
        yes = sum(1 for r in results if r[3] == "Yes")
        no = sum(1 for r in results if r[3] == "No")
        na = sum(1 for r in results if r[3] == "N/A")
        f.write(f"## Summary\n\n")
        f.write(f"- ✅ Yes: {yes}/{len(results)}\n")
        f.write(f"- ❌ No: {no}/{len(results)}\n")
        f.write(f"- ➖ N/A: {na}/{len(results)}\n\n")
        
        current_fr = None
        for r in results:
            if r[0] != current_fr:
                current_fr = r[0]
                f.write(f"\n## {current_fr}\n\n")
            sym = "✅" if r[3] == "Yes" else ("❌" if r[3] == "No" else "➖")
            f.write(f"- {sym} **{r[1]}** {r[2]}\n")
            if len(r) > 4 and r[4]:
                f.write(f"  - _{r[4]}_\n")
        
        f.write(f"\n---\n\n")
        f.write(f"For checklist rationale see <https://aem.lri.com.br/en-us/whitepapers/wp03-iec-62443-sl2-checklist>\n")
    
    print(f"\n✓ Report saved to {out}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--device-name", required=True)
    p.add_argument("--output", default="compliance-report.md")
    sys.exit(run(p.parse_args())) if False else None
    
    import sys
    args = p.parse_args()
    sys.exit(run(args))
