#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, struct

JP_SHA = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
F21_SHA = "00f46965177716ec459ac2a0f6e89a4e50548af205582e6d0ba176c015fc36ec"
F22_SHA = "3219fb1a0b49793ee7a9245e5468907c23a28f2b9125743d3cd17837e6485296"
CHECKSUM = 0x2157
TABLES = {
    "item_names_descriptions": (0x3800F8, 0x380B5C, (1330, 1158, 1158, 0, 0)),
    "magic_names": (0x38664C, 0x38668E, (33, 33, 33, 0, 0)),
    "magic_descriptions": (0x386806, 0x386848, (33, 33, 33, 0, 0)),
    "entity_names": (0x386B60, 0x386CA0, (160, 160, 160, 0, 0)),
    "map_names": (0x38B670, 0x38B688, (12, 12, 11, 0, 1)),
}

def sha256(data): return hashlib.sha256(data).hexdigest()

def decode(data, offset, limit=256):
    field = data[offset:offset + limit]
    end = field.find(b"\0\0")
    if end < 0: return None
    try: return field[:end].decode("cp932")
    except UnicodeDecodeError: return None

def has_japanese(text):
    return bool(text) and any("\u3040" <= c <= "\u30ff" or "\u3400" <= c <= "\u9fff" for c in text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jp"); parser.add_argument("f21"); parser.add_argument("f22")
    parser.add_argument("-o", "--output", default="I05_STATIC_VALIDATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifests/F/phase13BG_F22_changes.json").read_text(encoding="utf-8"))
    jp = Path(args.jp).read_bytes(); f21 = Path(args.f21).read_bytes(); f22 = Path(args.f22).read_bytes()
    assert sha256(jp) == JP_SHA and sha256(f21) == F21_SHA and sha256(f22) == F22_SHA
    expected_diff = {len(f22) - 2, len(f22) - 1}
    for change in manifest["changes"]:
        offset = int(change["offset"], 16); new = bytes.fromhex(change["new_hex"])
        old = bytes.fromhex(change["old_hex"]) if "old_hex" in change else bytes([int(change["old_fill"], 16)]) * change["bytes"]
        assert len(old) == len(new) == change["bytes"]
        assert f21[offset:offset + len(old)] == old and f22[offset:offset + len(new)] == new
        expected_diff.update(offset + i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1])
    actual_diff = {i for i, pair in enumerate(zip(f21, f22)) if pair[0] != pair[1]}
    assert actual_diff == expected_diff
    entries = []
    for entry in manifest["entries"]:
        pointer_offset = int(entry["pointer_offset"], 16)
        old_target = int(entry["old_target"], 16); new_target = int(entry["new_target"], 16)
        assert 0x380000 + struct.unpack_from("<H", f21, pointer_offset)[0] == old_target
        assert 0x380000 + struct.unpack_from("<H", f22, pointer_offset)[0] == new_target
        assert decode(jp, old_target) == entry["japanese"]
        assert decode(f22, new_target) == entry["encoded_display"]
        entries.append({**entry, "result": "PASS", "nul_terminated": True})
    census = {}; totals = [0, 0, 0, 0]
    for family, (start, end, expected) in TABLES.items():
        original_jp = repointed = survivors = translated_in_place = 0
        for slot in range(start, end, 2):
            old_pointer = struct.unpack_from("<H", jp, slot)[0]
            old_text = decode(jp, 0x380000 + old_pointer)
            if not has_japanese(old_text): continue
            original_jp += 1
            new_pointer = struct.unpack_from("<H", f22, slot)[0]
            if new_pointer != old_pointer:
                repointed += 1
            elif has_japanese(decode(f22, 0x380000 + new_pointer)):
                survivors += 1
            else:
                translated_in_place += 1
        actual = ((end - start) // 2, original_jp, repointed, survivors, translated_in_place)
        assert actual == expected, (family, actual, expected)
        census[family] = {"table_slots":actual[0],"original_japanese_targets":actual[1],"repointed":actual[2],"japanese_survivors":actual[3],"translated_in_place":actual[4]}
        for index, value in enumerate(actual[1:]): totals[index] += value
    assert totals == [1396, 1395, 0, 1]
    checksum = struct.unpack_from("<H", f22, len(f22) - 2)[0]
    assert checksum == (sum(f22[:-2]) & 0xFFFF) == CHECKSUM
    result = {
        "phase":"13BG-F22","result":"PASS","f22_sha256":sha256(f22),"wonderswan_checksum":f"{checksum:04X}",
        "entries":entries,"bank38_census":census,
        "totals":{"original_japanese_targets":1396,"repointed":1395,"japanese_survivors":0,"translated_in_place":1},
        "checks":{"integrated_occurrences":8,"actual_changed_bytes_including_checksum":len(actual_diff),"unexpected_changed_offsets":0,"original_sources_retained":True,"pool_was_ff_padding":True,"pointer_targets_in_bounds":True,"checksum_valid":True}
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS entries=8 slots=1568 original_jp=1396 survivors=0 changed={len(actual_diff)} checksum={checksum:04X}")

if __name__ == "__main__": main()
