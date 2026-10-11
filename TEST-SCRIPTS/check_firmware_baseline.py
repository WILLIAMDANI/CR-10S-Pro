#!/usr/bin/env python3
"""Fail CI when reviewed configuration declarations regress.

This checks source declarations, not preprocessor evaluation or printer behavior.
A real PlatformIO build and per-artifact physical regression run are also required.
Intentional baseline changes require a reviewed rationale and new printer results.
"""
import argparse
import re
from pathlib import Path


def declarations(path):
    text = re.sub(r'/\*.*?\*/', '', path.read_text(), flags=re.S)
    result = {}
    for line in text.splitlines():
        match = re.match(r'\s*#define\s+(\w+)\s*(.*?)\s*$', line.split('//', 1)[0])
        if match:
            name, value = match.groups()
            result.setdefault(name, []).append(value.strip())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    configs = {
        'Marlin/Configuration.h': {
            'MOTHERBOARD': 'BOARD_BTT_SKR_MINI_E3_V3_0',
            'SERIAL_PORT': '2', 'SERIAL_PORT_2': '-1', 'BAUDRATE': '115200',
            'INVERT_Z_DIR': 'true', 'Z_MIN_PROBE_ENDSTOP_INVERTING': 'false',
            'Z_MIN_PROBE_PIN': 'PC15', 'USE_PROBE_FOR_Z_HOMING': '',
            'FIX_MOUNTED_PROBE': '', 'Z_SAFE_HOMING': '',
            'Z_MIN_PROBE_REPEATABILITY_TEST': '',
            'THERMAL_PROTECTION_HOTENDS': '', 'THERMAL_PROTECTION_BED': '',
            'PIDTEMP': '', 'EEPROM_SETTINGS': '', 'SDSUPPORT': '',
            **{f'{axis}_DRIVER_TYPE': 'TMC2209' for axis in ('X', 'Y', 'Z', 'E0')},
        },
        'Marlin/Configuration_adv.h': {
            'E0_AUTO_FAN_PIN': 'FAN1_PIN', 'USE_CONTROLLER_FAN': '',
            'CONTROLLER_FAN_PIN': 'FAN2_PIN', 'EXTRUDER_AUTO_FAN_TEMPERATURE': '50',
            'X_CURRENT': '800', 'Y_CURRENT': '800', 'Z_CURRENT': '1000', 'E0_CURRENT': '800',
            'EMERGENCY_PARSER': '', 'USE_WATCHDOG': '',
            'AUTO_REPORT_POSITION': '', 'AUTO_REPORT_TEMPERATURES': '',
            'EXTENDED_CAPABILITIES_REPORT': '', 'M115_GEOMETRY_REPORT': '',
            'M114_DETAIL': '', 'REPORT_FAN_CHANGE': '',
            'HOST_ACTION_COMMANDS': '', 'HOST_PROMPT_SUPPORT': '',
            'HOST_STATUS_NOTIFICATIONS': '', 'SERIAL_FLOAT_PRECISION': '4',
            'LONG_FILENAME_HOST_SUPPORT': '', 'AUTO_REPORT_SD_STATUS': '',
        },
        'Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h': {
            'Z_MIN_PROBE_PIN': 'PC15', 'HEATER_0_PIN': 'PC8', 'HEATER_BED_PIN': 'PC9',
            'FAN0_PIN': 'PC6', 'FAN1_PIN': 'PC7', 'FAN2_PIN': 'PB15',
            'TEMP_0_PIN': 'PA0', 'TEMP_BED_PIN': 'PC4',
        },
    }
    forbidden = {
        'Marlin/Configuration.h': ('USE_ZMIN_PLUG', 'Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN',
                                   'BLTOUCH', 'PIDTEMPBED', 'FILAMENT_RUNOUT_SENSOR'),
        'Marlin/Configuration_adv.h': ('SENSORLESS_HOMING', 'SENSORLESS_PROBING',
                                       'Z_STEPPER_AUTO_ALIGN'),
    }
    failures = []
    checks = 0
    for filename, expected in configs.items():
        actual = declarations(args.root / filename)
        for name, value in expected.items():
            checks += 1
            if actual.get(name) != [value]:
                failures.append(f'{filename}: {name}: expected declaration {value!r}, got {actual.get(name)}')
        for name in forbidden.get(filename, ()):
            checks += 1
            if name in actual:
                failures.append(f'{filename}: {name} must remain disabled in this baseline')
    for failure in failures:
        print(f'FAIL: {failure}')
    print(f'{checks} declaration checks; {len(failures)} failures. Physical tests are separate.')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
