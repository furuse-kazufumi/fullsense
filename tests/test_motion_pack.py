# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from xml.dom import minidom


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tools" / "build_article_motion_pack.py"

spec = importlib.util.spec_from_file_location("build_article_motion_pack", SCRIPT)
assert spec is not None and spec.loader is not None
mp = importlib.util.module_from_spec(spec)
sys.modules["build_article_motion_pack"] = mp
spec.loader.exec_module(mp)


def test_wrap_escapes_metadata():
    svg = mp.wrap('A & B "title"', "desc with <angle> & amp", "<g/>")
    assert 'aria-label="A &amp; B &quot;title&quot;"' in svg
    assert "<title>A &amp; B &quot;title&quot;</title>" in svg
    assert "<desc>desc with &lt;angle&gt; &amp; amp</desc>" in svg


def test_frame_title_escapes_visible_text():
    fragment = mp.frame_title('A < B & C', 'quote " here & there')
    assert "A &lt; B &amp; C" in fragment
    assert 'quote &quot; here &amp; there' in fragment


def test_motion_pack_main_writes_expected_svgs(tmp_path, monkeypatch):
    monkeypatch.setattr(mp, "OUT", tmp_path)
    rc = mp.main()
    assert rc == 0

    generated = sorted(tmp_path.glob("*.svg"))
    assert [p.name for p in generated] == sorted(mp.ARTS.keys())

    for path in generated:
        xml = path.read_text(encoding="utf-8")
        minidom.parseString(xml.encode("utf-8"))
        assert "<title>" in xml
        assert "<desc>" in xml
        assert "animateMotion" not in xml
        assert "<mpath" not in xml


def test_loop_gate_warning_bar_is_authored_dim():
    svg = mp.loop_observe_gate_repair()
    assert '<g fill="#ef476f" opacity="0.22">' in svg
    assert 'width="46" height="8" rx="4" opacity="0.22"' in svg
    assert 'values="0.22;0.95;0.22"' in svg


def test_rocket_cycle_is_static_safe():
    svg = mp.rocket_launch_land_cycle()
    assert 'id="rocket-phase-launch"' in svg
    assert 'id="rocket-phase-coast"' in svg
    assert 'id="rocket-phase-flip"' in svg
    assert 'id="rocket-phase-descent"' in svg
    assert 'id="rocket-phase-landing"' in svg
    assert 'transform="translate(136 208)"' in svg
    assert 'transform="translate(342 126) rotate(-22)"' in svg
    assert 'transform="translate(470 166) rotate(18)"' in svg
    assert 'transform="translate(584 206) rotate(8)"' in svg
    assert 'transform="translate(804 220)"' in svg
    assert 'id="rocket-animated-token"' in svg
