# Example: 48V Telecom Battery Bank Monitoring

Worked compliance checklist for a typical telecom site DC plant deployment using the LRI AEM-60DC8.

## Deployment context

- 8 strings of 48V VRLA batteries (8 channels × 4 cells)
- Site located in a Tier III edge data center
- Modbus RTU over RS-485 to Ignition SCADA at the NOC
- WireGuard tunnel from site router to centralized supervisor
- 12-month maintenance contract with the operator

## Checklist results

(Excerpt — see CHECKLIST.md for the full list)

### FR1 IAC
- ✅ **IAC-1.1** Globally unique S/N read-only on Modbus register 40029
- ✅ **IAC-1.2** Exposed via Modbus block read (registers 40029-40031)
- ✅ **IAC-2.1** Calibration menu requires 4-digit password (default 1000, forced change on commissioning)
- ✅ **IAC-3.1** Firmware verified via Ed25519 signature before boot
- ➖ **IAC-2.2** N/A — single-tenant deployment, no role separation required

### FR3 SI
- ✅ All 9 layers of boot validation passed during AT test
- ✅ Anti-rollback counter at TAMP backup register, max 65535
- ✅ Bootloader in isolated flash region (0x0800_0000-0x0800_3FFF)

### FR6 TRE
- ✅ Audit log of last 32 events accessible via Modbus 40100-40131
- ✅ Reset reason exposed on register 40036
- ➖ **TRE-3.1** N/A — site uses NTP via WireGuard tunnel, supervisor time sync only

## Summary

42/47 Yes • 0/47 No • 5/47 N/A (with rationale)

✓ Ready for IEC 62443-4-2 SL2 certification assessment
