# aem-iec62443-checklist

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IEC 62443](https://img.shields.io/badge/IEC-62443--4--2-blue.svg)](https://webstore.iec.ch/publication/34421)
[![SL Target](https://img.shields.io/badge/SL%20target-2-orange.svg)](https://aem.lri.com.br/en-us/whitepapers/wp03-iec-62443-sl2-checklist)

> A practical, vendor-agnostic checklist for applying **IEC 62443-4-2 Security Level 2** to industrial device integrations.

This repo contains:
- **CHECKLIST.md** — 47 concrete acceptance criteria mapped to IEC 62443-4-2 SL2 requirements
- **validator.py** — a script that walks a device through the checklist interactively and emits a compliance report
- **examples/** — worked examples for common deployment scenarios (telecom battery bank, solar string monitor, substation aux DC)

For the longer narrative behind each item (threat model, why this matters, what attackers actually do), see the full whitepaper at <https://aem.lri.com.br/en-us/whitepapers/wp03-iec-62443-sl2-checklist>.

## Why this exists

IEC 62443-4-2 is a 200+ page document. Most SCADA integrators read it once, declare "we are SL2 compliant," and move on. That works until something happens.

This checklist breaks the SL2 component requirements into 47 yes/no items that an integrator can actually verify on a deployed device, with rationale for each. It is **vendor-agnostic** — the rationale applies to any industrial device, not specifically to our hardware.

## How to use

### 1. Read the checklist

Start with `CHECKLIST.md`. It is organized by the 7 IEC 62443 Foundational Requirements:

1. Identification and Authentication Control (IAC) — 8 items
2. Use Control (UC) — 7 items
3. System Integrity (SI) — 9 items
4. Data Confidentiality (DC) — 5 items
5. Restricted Data Flow (RDF) — 6 items
6. Timely Response to Events (TRE) — 6 items
7. Resource Availability (RA) — 6 items

### 2. Run the interactive validator

```bash
python validator.py --device-name "MyDeviceXYZ" --output compliance-report.md
```

Walks you through each item, asks yes/no, generates a compliance report you can attach to acceptance documents.

### 3. Adapt the examples

The `examples/` directory has pre-filled checklists for:
- 48V telecom battery bank monitoring
- Solar PV string supervision
- Substation auxiliary DC system

These show what "compliant" answers look like in context.

## Disclaimer

This is a community contribution to the IEC 62443 implementation conversation. It is **not** an official certification, and following this checklist does not by itself certify a device under IEC 62443-4-2. Certification requires formal assessment by an accredited body.

The checklist was developed during the [LRI AEM-60DC8](https://aem.lri.com.br/en-us) firmware compliance work (firmware v1.03 targets IEC 62443-4-2 SL2). The lessons are generalized for vendor-agnostic use.

## Related resources

- [IEC 62443-4-2:2019 standard](https://webstore.iec.ch/publication/34421) — official source (paywall)
- [LRI Whitepaper: IEC 62443-4-2 SL2 in Practice](https://aem.lri.com.br/en-us/whitepapers/wp03-iec-62443-sl2-checklist) — narrative context
- [aem-modbus-simulator](https://github.com/leaberg69/aem-modbus-simulator) — slave simulator for integration testing
- [aem-modbus-cli](https://github.com/leaberg69/aem-modbus-cli) — Modbus diagnostic CLI

## License

MIT — see [LICENSE](LICENSE).

## About

Maintained by [LRI Automação Industrial](https://lri.com.br), a Brazilian engineering firm. Headquartered in Porto Alegre/RS with a branch in Navegantes/SC. We make industrial DC monitoring hardware (the AEM family) that targets IEC 62443-4-2 SL2 compliance.
