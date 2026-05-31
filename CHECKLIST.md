# IEC 62443-4-2 SL2 — Integrator Checklist

> 47 concrete acceptance criteria for SCADA integrators verifying SL2 compliance on industrial devices.

Each item is yes/no. "Yes" = compliant. "N/A" with rationale = also acceptable. "No" without remediation plan = blocker.

## FR1 — Identification and Authentication Control (IAC)

### IAC-1. Unique device identity
- [ ] Device has a globally unique identifier (serial number, MAC, hardware ID) that is read-only and cannot be cloned by software.
- [ ] The identity is exposed via a documented interface (Modbus register, REST endpoint, MQTT topic) so the supervisor can audit.

### IAC-2. Authentication of human users
- [ ] Configuration/calibration menus require authentication (password, token, or physical key combination).
- [ ] Default credentials are forced to change on first commissioning.

### IAC-3. Authentication of software/processes
- [ ] Firmware updates require cryptographic signature verification (Ed25519, ECDSA P-256, or equivalent).
- [ ] Signing key rotation is documented and tested.

### IAC-4. Account management
- [ ] At least two roles exist: operator (read-only) and engineer (configuration).
- [ ] Account changes (create, modify, disable) are auditable in the device logs.

## FR2 — Use Control (UC)

### UC-1. Authorization enforcement
- [ ] Operator role cannot modify thresholds, baudrates, or slave IDs.
- [ ] Engineer role actions are logged with timestamp and user identity.

### UC-2. Wireless use control
- [ ] If wireless interfaces are present, they can be disabled by configuration.
- [ ] Wireless authentication uses at minimum WPA2-Enterprise or equivalent.

### UC-3. Mobile code restrictions
- [ ] Device does not execute dynamically loaded code from untrusted sources.
- [ ] No interpreter (Lua, Python, JavaScript) is exposed by default.

### UC-4. Session management
- [ ] Configuration sessions time out after a documented period of inactivity (≤15 min recommended).

## FR3 — System Integrity (SI)

### SI-1. Communication integrity
- [ ] Modbus RTU CRC validation is enforced; frames with bad CRC are silently dropped (not echoed).
- [ ] Out-of-band integrity check available (e.g., periodic counter exposed via Modbus that increments with each frame).

### SI-2. Malicious code protection
- [ ] Firmware signature verification is **enforced at boot**, not just at update time.
- [ ] Anti-rollback protection prevents downgrades to older signed-but-vulnerable versions.

### SI-3. Boot integrity (anti-brick)
- [ ] Bootloader is in a flash region that the update channel cannot write to.
- [ ] Failed firmware validation results in update mode, never in inoperability.

### SI-4. Boot validation chain (recommended 9-layer)
- [ ] Magic word check
- [ ] Header version check
- [ ] Header CRC
- [ ] Hardware ID match
- [ ] Payload size sanity
- [ ] Payload CRC
- [ ] Vector table sanity
- [ ] Trailer seal
- [ ] Cryptographic signature

### SI-5. Persistent anti-rollback counter
- [ ] Counter stored in battery-backed register (e.g., STM32 TAMP) that survives reset and power cycle.
- [ ] Counter saturates at a documented maximum (typically 16-bit unsigned = 65,535).

## FR4 — Data Confidentiality (DC)

### DC-1. Cryptographic key management
- [ ] Signing keys held in hardware (Yubikey, HSM, or equivalent) — never on developer laptops.
- [ ] Key rotation procedure is documented and exercised at least annually.

### DC-2. Sensitive telemetry handling
- [ ] No personally identifiable information (PII) is collected by the device.
- [ ] Diagnostic data exported via Modbus does not contain credentials or session tokens.

### DC-3. Default-deny network exposure
- [ ] Device does not phone home to manufacturer servers by default.
- [ ] All outbound connections require explicit configuration.

## FR5 — Restricted Data Flow (RDF)

### RDF-1. Network segmentation
- [ ] Device documents which network segments it can be deployed on (DMZ, OT, IT).
- [ ] No bridging functionality between segments.

### RDF-2. Zone boundary protection
- [ ] Galvanic isolation between field-side (high voltage, untrusted) and logic-side (MCU, supervisor) — recommended ≥5000 VAC rms.
- [ ] Opto-isolated digital inputs.

### RDF-3. Authoritative configuration source
- [ ] Configuration changes via Modbus are authenticated (or restricted to engineer role).
- [ ] Changes are persisted to non-volatile storage with documented write count limits.

## FR6 — Timely Response to Events (TRE)

### TRE-1. Audit log
- [ ] Device maintains an audit log of security-relevant events (auth failures, config changes, firmware updates).
- [ ] Log is queryable via Modbus or equivalent protocol.

### TRE-2. Forensic telemetry
- [ ] Post-incident data (reset reason, HardFault traces, RTOS health, NACK counters) accessible via Modbus.
- [ ] No cloud or physical access required to retrieve forensic data.

### TRE-3. Time stamping
- [ ] Device has a real-time clock with battery backup OR receives time from supervisor.
- [ ] Events in audit log are timestamped.

## FR7 — Resource Availability (RA)

### RA-1. Denial of service protection
- [ ] Modbus implementation rate-limits malformed requests.
- [ ] Single failed authentication does not block subsequent attempts.

### RA-2. Resource exhaustion protection
- [ ] Configurable maximum concurrent connections.
- [ ] Watchdog timer resets the device on hang.

### RA-3. Backup and restore
- [ ] Configuration can be exported and re-imported (e.g., via Modbus block write).
- [ ] Factory reset is documented and reachable via physical means.

---

## Scoring

- **47/47 yes** = ready for IEC 62443-4-2 SL2 certification assessment
- **40-46 yes** = address gaps before assessment
- **<40 yes** = SL2 is not the right target yet; reassess as SL1

## Notes for SCADA integrators

This checklist is for **integration acceptance**, not for certification. Formal IEC 62443-4-2 certification requires assessment by an accredited body. However, an integrator who walks a device through this list during commissioning will catch the most common security gaps that cause real incidents.

For the detailed rationale on each item — including the threat model and what attackers actually exploit when these controls are missing — see the [LRI whitepaper "IEC 62443-4-2 SL2 in Practice"](https://aem.lri.com.br/en-us/whitepapers/wp03-iec-62443-sl2-checklist).
