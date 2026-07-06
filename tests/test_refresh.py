"""Staleness-report tests (`kp-build refresh` engine) — offline, fake S2 transports."""

import json

import pytest

from kp_build.assemble import assemble
from kp_build.refresh import refresh
from kp_build.schema import Package, Paper, Verification


def _V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-01-15")


def _pkg(tmp_path, *, built, papers=None):
    """A real assembled package (real assemble(), like the report/deepen tests build theirs)."""
    papers = papers if papers is not None else [
        Paper(cite_key="seed2025", title="Seed Paper", year=2025, arxiv_id="2501.00001",
              verified=_V())]
    pkg = Package(topic="test topic", scope="test scope", papers=papers)
    return assemble(pkg, tmp_path / "kp", built=built)


def _s2(cands):
    """An S2 references payload (the shape tests/test_deepen.py fakes). Returning the SAME payload
    for both directions is safe: the citations direction looks for 'citingPaper', finds nothing,
    and contributes zero candidates."""
    rows = [{"citedPaper": {"title": c.get("title", ""), "year": c.get("year"),
                            "externalIds": {"ArXiv": c.get("arxiv_id", ""),
                                            "DOI": c.get("doi", "")}}} for c in cands]
    return json.dumps({"data": rows})


def _get(cands):
    payload = _s2(cands)
    return lambda u: payload


# ── the tri-state decision ───────────────────────────────────────────────────────────


def test_stale_when_expansion_finds_post_build_paper(tmp_path):
    # built 2026-01, as_of 2026-07 (age 6 <= 30) — but a 2026-03 arXiv candidate post-dates the build
    out = _pkg(tmp_path, built="2026-01-15")
    get = _get([{"title": "Newer Work", "year": 2026, "arxiv_id": "2603.00042"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["decision"] == "stale" and rep["new_since_build"] == 1
    assert rep["candidates"][0]["arxiv_id"] == "2603.00042"
    assert rep["age_months"] == 6 and rep["spine_size"] == 1
    assert "post-dat" in rep["reason"]


def test_fresh_when_all_candidates_pre_date_build(tmp_path):
    # same clock, but every candidate PRE-dates the build -> nothing new, age 6 <= 30 -> fresh
    out = _pkg(tmp_path, built="2026-01-15")
    get = _get([{"title": "Old Classic", "year": 2020, "arxiv_id": "2001.00007"},
                {"title": "Older Still", "year": 2017, "arxiv_id": "1706.03762"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["decision"] == "fresh" and rep["new_since_build"] == 0
    assert rep["total_candidates"] == 2 and rep["candidates"] == []


def test_stale_by_age_alone(tmp_path):
    # built 2023-01, as_of 2026-07 -> 42 months > 30: stale even though nothing new surfaced
    out = _pkg(tmp_path, built="2023-01-15")
    get = _get([{"title": "Old Classic", "year": 2020, "arxiv_id": "2001.00007"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["decision"] == "stale" and rep["new_since_build"] == 0
    assert rep["age_months"] == 42 and "age" in rep["reason"]


def test_inconclusive_on_zero_candidates(tmp_path):
    # expand() degrades silently per-seed, so a ZERO total must abstain, never read as 'fresh'
    out = _pkg(tmp_path, built="2026-01-15")
    rep = refresh(out, as_of="2026-07", get=lambda u: json.dumps({"data": []}))
    assert rep["decision"] == "inconclusive" and rep["total_candidates"] == 0
    assert "re-run" in rep["reason"]


# ── ValueErrors (the CLI maps these to exit 2) ───────────────────────────────────────


def test_bad_as_of_raises(tmp_path):
    out = _pkg(tmp_path, built="2026-01-15")
    for bad in ("2026-13", "yesterday", ""):
        with pytest.raises(ValueError):
            refresh(out, as_of=bad, get=_get([]))


def test_no_verified_seeds_raises(tmp_path):
    # a spine paper must be verified AND carry an id: unverified-with-id and verified-without-id
    # both fail to seed the expansion -> clear ValueError, not a silent empty report
    papers = [Paper(cite_key="unv", title="Unverified", arxiv_id="2501.00001"),
              Paper(cite_key="noid", title="Verified But Id-less", verified=_V())]
    out = _pkg(tmp_path, built="2026-01-15", papers=papers)
    with pytest.raises(ValueError, match="no verified spine"):
        refresh(out, as_of="2026-07", get=_get([]))


def test_not_a_package_raises(tmp_path):
    with pytest.raises(ValueError, match="wikillm.json"):
        refresh(tmp_path, as_of="2026-07", get=_get([]))


# ── partition honesty ────────────────────────────────────────────────────────────────


def test_undated_candidates_counted_not_newified(tmp_path):
    # no arXiv YYMM and no year = no dating signal: counted in undated_candidates, never in
    # new_since_build and never silently dropped (the no-silent-caps rule)
    out = _pkg(tmp_path, built="2026-01-15")
    get = _get([{"title": "Journal Paper, No Date", "year": None, "doi": "10.1234/undated"},
                {"title": "Newer Work", "year": 2026, "arxiv_id": "2603.00042"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["undated_candidates"] == 1 and rep["new_since_build"] == 1
    assert rep["total_candidates"] == 2
    assert all(c["doi"] != "10.1234/undated" for c in rep["candidates"])


def test_year_only_candidate_is_coarse_strict_greater(tmp_path):
    # a year-only (non-arXiv) candidate counts as post-build only if year > built's YEAR:
    # same-year is NOT new (it may pre-date the build month), next-year is
    out = _pkg(tmp_path, built="2026-01-15")
    get = _get([{"title": "Same Year DOI", "year": 2026, "doi": "10.1/same"},
                {"title": "Next Year DOI", "year": 2027, "doi": "10.1/next"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["new_since_build"] == 1 and rep["candidates"][0]["doi"] == "10.1/next"
    assert rep["undated_candidates"] == 0


def test_candidates_already_in_package_are_skipped(tmp_path):
    # a candidate whose id the package already holds (even UNVERIFIED) is not "new"
    papers = [Paper(cite_key="seed2025", title="Seed", year=2025, arxiv_id="2501.00001", verified=_V()),
              Paper(cite_key="held", title="Already Held", year=2026, arxiv_id="2603.00042")]
    out = _pkg(tmp_path, built="2026-01-15", papers=papers)
    get = _get([{"title": "Already Held", "year": 2026, "arxiv_id": "2603.00042"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["total_candidates"] == 0 and rep["new_since_build"] == 0
    assert rep["decision"] == "inconclusive"      # everything skipped -> zero-total abstain


# ── report contract ──────────────────────────────────────────────────────────────────


def test_report_keys_and_reprobe_prompt(tmp_path):
    out = _pkg(tmp_path, built="2026-01-15")
    rep = refresh(out, as_of="2026-07-04", get=_get([{"title": "N", "year": 2026,
                                                      "arxiv_id": "2603.00042"}]))
    for k in ("topic", "built", "as_of", "age_months", "spine_size", "seeds", "candidates",
              "new_since_build", "undated_candidates", "total_candidates", "decision", "reason",
              "reprobe_prompt"):
        assert k in rep, k
    assert rep["topic"] == "test topic" and rep["seeds"] == ["2501.00001"]
    assert "test topic" in rep["reprobe_prompt"] and "## Citations" in rep["reprobe_prompt"]
    assert set(rep["candidates"][0]) == {"title", "year", "arxiv_id", "doi", "via"}


def test_unparseable_built_is_inconclusive_never_fresh(tmp_path):
    # built missing/garbled -> NEITHER staleness signal can run: the age test can never fire and no
    # candidate can ever count as post-build, so 'fresh' here would be fail-OPEN — a package with a
    # broken 'built' field would read fresh forever. The honest verdict is INCONCLUSIVE (exit 3 at
    # the CLI); the reason reports ALL candidates unjudgeable, and a DATED candidate stays out of
    # undated_candidates (it carries a date — the build side is what's broken).
    out = _pkg(tmp_path, built="unknown")
    get = _get([{"title": "Dated", "year": 2026, "arxiv_id": "2603.00042"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["age_months"] is None and rep["new_since_build"] == 0
    assert rep["decision"] == "inconclusive"
    assert "built" in rep["reason"] and "re-run" in rep["reason"]
    assert rep["undated_candidates"] == 0 and rep["total_candidates"] == 1


def test_future_built_is_inconclusive_never_fresh(tmp_path):
    # a FUTURE 'built' (typo, clock skew) is the same fail-open one door over: age can never exceed
    # the threshold and no candidate can post-date the build, so 'fresh' would again be forever.
    out = _pkg(tmp_path, built="2027-01-15")
    get = _get([{"title": "Dated", "year": 2026, "arxiv_id": "2603.00042"}])
    rep = refresh(out, as_of="2026-07", get=get)
    assert rep["decision"] == "inconclusive"
    assert rep["age_months"] == -6 and rep["new_since_build"] == 0
    assert "future" in rep["reason"]


def test_missing_built_key_is_inconclusive_even_with_zero_candidates(tmp_path):
    # no 'built' at all + a quiet expansion: still inconclusive (both the broken-built and the
    # zero-candidate abstains point the same way — never a defaulted 'fresh')
    out = _pkg(tmp_path, built="")
    rep = refresh(out, as_of="2026-07", get=_get([]))
    assert rep["decision"] == "inconclusive" and rep["age_months"] is None


# ── the CLI wrapper: exit codes mirror probe's tri-state ─────────────────────────────


def _cli_result(decision):
    return {"topic": "t", "built": "2026-01-15", "as_of": "2026-07", "age_months": 6,
            "spine_size": 1, "seeds": ["2501.00001"], "candidates": [], "new_since_build": 0,
            "undated_candidates": 0, "total_candidates": 0, "decision": decision,
            "reason": "because", "reprobe_prompt": "p"}


def test_cli_refresh_exit_codes(monkeypatch, capsys):
    import kp_build.refresh as R
    from kp_build.cli import main
    monkeypatch.setattr(R, "refresh", lambda *a, **k: _cli_result("fresh"))
    assert main(["refresh", "/pkg"]) == 0
    assert "FRESH" in capsys.readouterr().out
    monkeypatch.setattr(R, "refresh", lambda *a, **k: _cli_result("stale"))
    assert main(["refresh", "/pkg"]) == 1
    assert "STALE" in capsys.readouterr().out
    monkeypatch.setattr(R, "refresh", lambda *a, **k: _cli_result("inconclusive"))
    assert main(["refresh", "/pkg"]) == 3       # distinct from usage/IO errors (2)
    assert "INCONCLUSIVE" in capsys.readouterr().out


def test_cli_refresh_inconclusive_skips_the_refresh_workflow_hint(monkeypatch, capsys):
    # an inconclusive run's next step is in its reason (fix the manifest / re-run) — printing the
    # "re-probe + fold candidates in" workflow hint there would point at the wrong door
    import kp_build.refresh as R
    from kp_build.cli import main
    monkeypatch.setattr(R, "refresh", lambda *a, **k: _cli_result("inconclusive"))
    main(["refresh", "/pkg"])
    assert "next:" not in capsys.readouterr().err
    monkeypatch.setattr(R, "refresh", lambda *a, **k: _cli_result("fresh"))
    main(["refresh", "/pkg"])
    assert "next: re-probe" in capsys.readouterr().err


def test_cli_refresh_passes_flags_and_defaults_the_clock(monkeypatch):
    import kp_build.refresh as R
    from kp_build.cli import main
    seen = {}
    def spy(pkg, *, as_of, recency_months, per_seed, **kw):
        seen.update(pkg=pkg, as_of=as_of, recency_months=recency_months, per_seed=per_seed)
        return _cli_result("fresh")
    monkeypatch.setattr(R, "refresh", spy)
    main(["refresh", "/pkg", "--as-of", "2026-07", "--recency-months", "12", "--limit", "5"])
    assert seen == {"pkg": "/pkg", "as_of": "2026-07", "recency_months": 12, "per_seed": 5}
    main(["refresh", "/pkg"])                   # no --as-of -> the CLI supplies today, never the engine
    assert seen["as_of"] and seen["as_of"] != "2026-07" and len(seen["as_of"]) == 10


def test_cli_refresh_missing_package_is_exit_2(tmp_path, capsys):
    from kp_build.cli import main
    assert main(["refresh", str(tmp_path / "nope")]) == 2   # ValueError -> usage/IO backstop
    assert "error" in capsys.readouterr().err
