"""V2-a: the pluggable verifier seam — §4.0 widen the Verification contract from citation-shaped
to verifier-agnostic, WITHOUT changing academic-pack behavior.

TDD regression net:
- characterization tests lock the CURRENT academic ship-gate behavior (green on the pre-refactor code);
- the widened-contract tests are RED until §4.0 lands, then green — the academic ones must stay green.
"""
from pathlib import Path

from kp_build.schema import (
    Package, Paper, Claim, Verification, paper_to_md, paper_from_md,
    claim_to_md, claim_from_md,
)
from kp_build.assemble import assemble


# ── V2-b: doc-grounding wired into build — STEP 1: the grounding directive round-trips ───────

def test_claim_grounding_directive_round_trips():
    """A `grounding` directive ({source, supporting_passage}) must survive claim_to_md ->
    claim_from_md unchanged — symmetric round-trip, exactly like the `execution` directive. The write
    side is free (asdict); the read side (claim_from_md) hand-lists keys and must include `grounding`."""
    c = Claim(id="g1", statement="HTTP defines GET.", paper="", supporting_passage="the GET method.",
              grounding={"source": "RFC9110", "supporting_passage": "The GET method requests transfer."})
    c2 = claim_from_md(claim_to_md(c))
    assert c2.grounding == {"source": "RFC9110", "supporting_passage": "The GET method requests transfer."}
    # academic/execution claims keep an empty grounding directive (no regression)
    assert claim_from_md(claim_to_md(Claim(id="a", statement="s", paper="p1", supporting_passage="x"))).grounding == {}


def test_claim_judgment_directive_round_trips():
    """A `judgment` directive ({task, answer, baseline, rounds}) round-trips — the recorded blind-panel
    the build replays through JudgeVerifier. rounds is the per-comparison slot winners ('a'/'b'/'tie')."""
    c = Claim(id="j1", statement="approach A beats B", paper="", supporting_passage="x",
              judgment={"task": "make a clean title card", "answer": "A", "baseline": "B",
                        "rounds": ["a", "b", "a", "b"]})
    c2 = claim_from_md(claim_to_md(c))
    assert c2.judgment == {"task": "make a clean title card", "answer": "A", "baseline": "B",
                           "rounds": ["a", "b", "a", "b"]}
    assert claim_from_md(claim_to_md(Claim(id="a", statement="s", paper="p1", supporting_passage="x"))).judgment == {}


def test_verify_judgment_claims_replays_recorded_panel_and_defeats_fakes():
    """The build replays the recorded slot-vote panel through JudgeVerifier (deterministic). A genuine
    answer-favoring panel ships (judged-better); a FAKED uniform panel nets to a tie via the A/B
    alternation (an author can't hand-write 'answer wins'); a baseline-favoring panel is judged-worse."""
    from kp_build.verifier import verify_judgment_claims
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="win", statement="A>B", paper="", supporting_passage="x",
              judgment={"task": "t", "answer": "A", "baseline": "B", "rounds": ["a", "b", "a", "b"]}),
        Claim(id="fake", statement="A>B", paper="", supporting_passage="x",
              judgment={"task": "t", "answer": "A", "baseline": "B", "rounds": ["a", "a", "a", "a"]}),
        Claim(id="lose", statement="A<B", paper="", supporting_passage="x",
              judgment={"task": "t", "answer": "A", "baseline": "B", "rounds": ["b", "a", "b", "a"]}),
    ])
    summ = verify_judgment_claims(pkg, today="2026-01-01")
    by = {c.id: c.verified for c in pkg.claims}
    assert by["win"].exists is True and by["win"].status == "judged-better" and by["win"].kind == "judgment"
    assert by["fake"].exists is False and by["fake"].status == "judged-tie"      # alternation defeats the fake
    assert by["lose"].exists is False and by["lose"].status == "judged-worse"
    assert summ == {"judgment_total": 3, "judgment_verified": 1}

def test_verify_judgment_claims_leaves_other_claims_untouched():
    from kp_build.verifier import verify_judgment_claims
    pkg = Package(topic="t", scope="s", papers=[Paper(cite_key="p1", title="T")],
                  claims=[Claim(id="c1", statement="s", paper="p1", supporting_passage="x")])
    assert verify_judgment_claims(pkg, today="x") == {"judgment_total": 0, "judgment_verified": 0}
    assert pkg.claims[0].verified.status == "unverified"

def test_verify_judgment_claims_abstains_on_malformed_rounds():
    """Defense-in-depth: even bypassing _load, a length-1 or odd-length recorded panel
    must NEVER ship — it abstains (unverifiable), not judged-better. The replay must not pad a missing
    slot with a free 'tie' (the ['a'] fake) nor truncate a balancing vote (the odd-length tie laundering)."""
    from kp_build.verifier import verify_judgment_claims
    for bad in (["a"], ["a", "tie", "b"], [], ["a", "a", "a"]):
        pkg = Package(topic="t", scope="s", papers=[], claims=[
            Claim(id="x", statement="s", paper="", supporting_passage="x",
                  judgment={"task": "t", "answer": "A", "baseline": "B", "rounds": bad})])
        verify_judgment_claims(pkg)
        v = pkg.claims[0].verified
        assert v.exists is False and v.status == "unverifiable", f"{bad} should abstain, got {v.status}"
    # a genuine EVEN panel still ships
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="x", statement="s", paper="", supporting_passage="x",
              judgment={"task": "t", "answer": "A", "baseline": "B", "rounds": ["a", "b"]})])
    verify_judgment_claims(pkg)
    assert pkg.claims[0].verified.status == "judged-better"


# ── characterization: lock current academic behavior (GREEN before AND after §4.0) ──────────

def test_assemble_ship_gate_handles_academic_claims_without_per_claim_verdict(tmp_path: Path):
    """The ship gate is PAPER-level (`p.verified.exists`); academic claims carry NO own verdict.
    The §4.1/§4.2 ship-gate generalization must keep working for claims with no per-claim verdict —
    i.e. it must never AttributeError reading `claim.verified`. This locks that contract."""
    pkg = Package(
        topic="t", scope="s",
        papers=[
            Paper(cite_key="real", title="Real",
                  verified=Verification(exists=True, status="verified", via="arxiv",
                                        canonical_title="Real", checked="2026-01-01")),
            Paper(cite_key="fake", title="Fake",
                  verified=Verification(exists=False, status="not-found")),
        ],
        claims=[
            Claim(id="c1", statement="kept", paper="real", supporting_passage="p1"),
            Claim(id="c2", statement="dropped", paper="fake", supporting_passage="p2"),
        ],
    )
    out = assemble(pkg, tmp_path, built="2026-01-01")
    assert (out / "claims" / "c1.md").exists()          # verified-anchored claim ships
    assert not (out / "claims" / "c2.md").exists()       # unverified-anchored claim dropped
    # the load-bearing invariant (behavioral): an academic claim ships purely via its PAPER —
    # its per-claim verdict stays at the default (exists=False) and is NOT relied on.
    assert pkg.claims[0].verified.exists is False


# ── §4.0: the widened, verifier-agnostic contract (RED until implemented) ────────────────────

def test_verification_is_verifier_agnostic():
    """A non-citation verifier (execution) records its kind + evidence and round-trips intact."""
    v = Verification(exists=True, status="verified", kind="execution",
                     via="hyperframes-cli@0.6.91",
                     evidence="lint:non_deterministic_code cleared; inspect:no overflow",
                     checked="2026-01-01")
    p = Paper(cite_key="hf-determinism-1", title="no Math.random", verified=v)
    back = paper_from_md(paper_to_md(p))
    assert back == p
    assert back.verified.kind == "execution"
    assert back.verified.evidence.startswith("lint:")


def test_verification_kind_defaults_to_existence_for_legacy_packages():
    """Academic packs are `kind='existence'` by default; legacy frontmatter with no `kind` reads back
    as existence — so old packages validate unchanged (the migration promise)."""
    assert Verification(exists=True, status="verified", via="arxiv").kind == "existence"
    p = Paper(cite_key="x", title="X",
              verified=Verification(exists=True, status="verified", via="arxiv", canonical_title="X"))
    back = paper_from_md(paper_to_md(p))
    assert back.verified.kind == "existence"
    assert back.verified.evidence == ""


def test_exists_remains_the_universal_ship_gate_across_kinds():
    """`exists` is the ship invariant for EVERY verifier kind, with the new execution statuses allowed."""
    assert Verification(exists=True, status="verified", kind="execution").exists is True
    assert Verification(exists=False, status="output-mismatch", kind="execution").exists is False
    assert Verification(exists=False, status="not-found", kind="grounding").exists is False


# ── §4.1: GoalMetric — KPI-anchored scope (RED until implemented) ─────────────────────────────

def test_goal_metric_carries_kpi_target_direction_and_oracle_kind():
    from kp_build.schema import GoalMetric
    gm = GoalMetric(name="water_absorption", description="equilibrium uptake",
                    baseline="7-8.5%", target="<0.5%", direction="lower", unit="%",
                    acceptance_threshold="0.5", measurement_method="ASTM D570", oracle_kind="none")
    assert gm.direction == "lower" and gm.oracle_kind == "none"


def test_goal_metric_from_dict_round_trips():
    from kp_build.schema import GoalMetric, goal_metric_from_dict
    gm = GoalMetric(name="strength", description="break force", direction="higher",
                    oracle_kind="grounding", unit="N")
    assert goal_metric_from_dict({"name": "strength", "description": "break force",
                                  "direction": "higher", "oracle_kind": "grounding", "unit": "N"}) == gm


def test_package_carries_goals_and_goal_metrics_default_empty():
    from kp_build.schema import GoalMetric
    assert Package(topic="t", scope="s").goal_metrics == []        # academic packs stay valid (optional)
    pkg = Package(topic="t", scope="s",
                  goals={"choose_mesh": "a material that survives wet weather and is rules-legal"},
                  goal_metrics=[GoalMetric(name="strength", direction="higher", oracle_kind="grounding")])
    assert pkg.goals["choose_mesh"].startswith("a material")
    assert pkg.goal_metrics[0].name == "strength"


# ── §4.2: Relation — first-class, KPI-anchored, verifiable edges (RED until implemented) ──────

def test_relation_is_kpi_anchored_and_carries_its_own_verdict():
    from kp_build.schema import Relation
    r = Relation(id="r1", source="c1", target="c2", type="tradeoff",
                 description="nylon strength trades against water absorption",
                 kpis=["strength", "water_absorption"],
                 verification=Verification(exists=True, status="verified", kind="grounding",
                                           evidence="quoted: amide H-bonds give tenacity AND uptake"))
    assert len(r.kpis) >= 2                       # a connection spans ≥2 KPIs (the spec's rule)
    assert r.verification.kind == "grounding"
    assert r.verification.exists is True


def test_relation_round_trips_through_md():
    from kp_build.schema import Relation, relation_to_md, relation_from_md
    r = Relation(id="r1", source="c1", target="c2", type="tradeoff", description="d",
                 kpis=["strength", "water_absorption"],
                 verification=Verification(exists=True, status="verified", kind="grounding",
                                           evidence="passage"))
    back = relation_from_md(relation_to_md(r))
    assert back == r


def test_package_carries_relations_default_empty():
    from kp_build.schema import Relation
    assert Package(topic="t", scope="s").relations == []          # optional — academic packs unaffected
    pkg = Package(topic="t", scope="s",
                  relations=[Relation(id="r1", source="c1", target="c2", type="tradeoff",
                                      kpis=["a", "b"])])
    assert pkg.relations[0].kpis == ["a", "b"]


# ── wiring: cli._load parse + assemble persist + digest CONTEXT (RED until wired) ─────────────

import json
import pytest


def _write(tmp_path, obj):
    f = tmp_path / "r.json"; f.write_text(json.dumps(obj)); return str(f)


_BASE = {
    "topic": "mesh", "scope": "s",
    "papers": [{"cite_key": "p1", "title": "T"}],
    "claims": [{"id": "c1", "statement": "a", "paper": "p1", "supporting_passage": "x"},
               {"id": "c2", "statement": "b", "paper": "p1", "supporting_passage": "y"}],
}


def test_load_parses_goals_metrics_and_relations(tmp_path):
    from kp_build.cli import _load
    rj = dict(_BASE,
              goals={"choose": "a wet-durable, rules-legal mesh"},
              goal_metrics=[{"name": "strength", "direction": "higher", "oracle_kind": "grounding"},
                            {"name": "water_absorption", "direction": "lower", "oracle_kind": "none"}],
              relations=[{"id": "r1", "source": "c1", "target": "c2", "type": "tradeoff",
                          "description": "strength trades against water", "kpis": ["strength", "water_absorption"]}])
    pkg = _load(_write(tmp_path, rj))
    assert pkg.goals["choose"].startswith("a wet")
    assert {gm.name for gm in pkg.goal_metrics} == {"strength", "water_absorption"}
    assert pkg.relations[0].kpis == ["strength", "water_absorption"]


def test_load_rejects_relation_with_under_two_kpis(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    rj = dict(_BASE, relations=[{"id": "r1", "source": "c1", "target": "c2", "kpis": ["only_one"]}])
    with pytest.raises(ResearchInputError, match="2 KPIs"):
        _load(_write(tmp_path, rj))


def test_load_rejects_relation_with_dangling_endpoint(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    rj = dict(_BASE, relations=[{"id": "r1", "source": "c1", "target": "nope", "kpis": ["a", "b"]}])
    with pytest.raises(ResearchInputError, match="resolves to no node"):
        _load(_write(tmp_path, rj))


# ── V2-b STEP 2: cli._load parses a grounding directive, enforces 3-way XOR + source path-safety ──

_GCLAIM = {"id": "g1", "statement": "GET requests transfer of a representation.", "supporting_passage": "GET",
           "grounding": {"source": "RFC9110",
                         "supporting_passage": "The GET method requests transfer of a current representation."}}

def test_load_accepts_grounding_directive_on_no_paper_claim(tmp_path):
    from kp_build.cli import _load
    pkg = _load(_write(tmp_path, dict(_BASE, claims=[_GCLAIM])))
    assert pkg.claims[0].grounding["source"] == "RFC9110"
    assert pkg.claims[0].grounding["supporting_passage"].startswith("The GET method")

def test_load_rejects_grounding_plus_paper(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = dict(_GCLAIM, paper="p1")
    with pytest.raises(ResearchInputError, match="more than one verification basis"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))

def test_load_rejects_grounding_plus_execution(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = dict(_GCLAIM, execution={"tool": "lint", "gate_code": "x", "artifact": "a/b"})
    with pytest.raises(ResearchInputError, match="more than one verification basis"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))

def test_load_rejects_grounding_source_path_escape(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = {"id": "g1", "statement": "s", "supporting_passage": "x",
           "grounding": {"source": "../../etc/passwd", "supporting_passage": "q"}}
    with pytest.raises(ResearchInputError, match="unsafe characters"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))

def test_load_rejects_grounding_missing_passage(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = {"id": "g1", "statement": "s", "supporting_passage": "x", "grounding": {"source": "RFC9110"}}
    with pytest.raises(ResearchInputError, match="supporting_passage"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))


# ── v2-b judgment wiring: cli._load parses the judgment directive + 4-way XOR + validation ────

_JCLAIM = {"id": "j1", "statement": "approach A>B", "supporting_passage": "x",
           "judgment": {"task": "make a clean card", "answer": "A", "baseline": "B",
                        "rounds": ["a", "b", "a", "b"]}}

def test_load_accepts_judgment_directive_on_no_paper_claim(tmp_path):
    from kp_build.cli import _load
    pkg = _load(_write(tmp_path, dict(_BASE, claims=[_JCLAIM])))
    assert pkg.claims[0].judgment["rounds"] == ["a", "b", "a", "b"]
    assert pkg.claims[0].judgment["answer"] == "A"

def test_load_rejects_judgment_plus_paper(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    with pytest.raises(ResearchInputError, match="more than one verification basis"):
        _load(_write(tmp_path, dict(_BASE, claims=[dict(_JCLAIM, paper="p1")])))

def test_load_rejects_judgment_missing_fields(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = {"id": "j1", "statement": "s", "supporting_passage": "x", "judgment": {"task": "t", "answer": "A"}}
    with pytest.raises(ResearchInputError, match="judgment"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))

def test_load_rejects_judgment_bad_rounds(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    bad = {"id": "j1", "statement": "s", "supporting_passage": "x",
           "judgment": {"task": "t", "answer": "A", "baseline": "B", "rounds": ["a", "x"]}}
    with pytest.raises(ResearchInputError, match="rounds"):
        _load(_write(tmp_path, dict(_BASE, claims=[bad])))

def test_load_rejects_judgment_odd_or_underlength_rounds(tmp_path):
    """Position-bias cancellation REQUIRES an even-length (>=2) panel — the answer must
    occupy slot a and slot b equally. Reject ['a'] (the cheapest fake, which padded to a phantom win) and
    any odd length (which truncated a balancing vote, laundering a tie into judged-better)."""
    from kp_build.cli import _load, ResearchInputError
    for bad_rounds in (["a"], ["a", "b", "a"], ["a", "tie", "b"]):
        bad = {"id": "j", "statement": "s", "supporting_passage": "x",
               "judgment": {"task": "t", "answer": "A", "baseline": "B", "rounds": bad_rounds}}
        with pytest.raises(ResearchInputError, match="EVEN number"):
            _load(_write(tmp_path, dict(_BASE, claims=[bad])))


# ── V2-b STEP 3: verify_grounding_claims sets per-claim verdicts from the pinned corpus ───────

def test_verify_grounding_claims_sets_verdicts_by_corpus_presence():
    """Mirrors verify_execution_claims: for each claim with a grounding directive, ground its passage
    against corpus[source] and set c.verified. Tri-state -> verified / ungrounded / unconfirmed, and a
    source missing from the corpus -> ungrounded-unreachable (a coverage debt, never laundered to verified)."""
    from kp_build.verifier import verify_grounding_claims
    sentence = "The GET method requests transfer of a current representation of the target resource."
    corpus = {"RFC9110": sentence}
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="ok", statement="s", paper="", supporting_passage="x",
              grounding={"source": "RFC9110", "supporting_passage": sentence}),
        Claim(id="para", statement="s", paper="", supporting_passage="x",
              grounding={"source": "RFC9110",
                         "supporting_passage": "GET asks the server to send back whatever currently exists there."}),
        Claim(id="frag", statement="s", paper="", supporting_passage="x",
              grounding={"source": "RFC9110", "supporting_passage": "GET method"}),
        Claim(id="missing", statement="s", paper="", supporting_passage="x",
              grounding={"source": "RFC9999", "supporting_passage": "Some full-length sentence not in any held corpus."}),
    ])
    summ = verify_grounding_claims(pkg, corpus=corpus, today="2026-01-01")
    by = {c.id: c.verified for c in pkg.claims}
    assert by["ok"].exists is True and by["ok"].status == "verified" and by["ok"].kind == "grounding"
    assert by["para"].exists is False and by["para"].status == "ungrounded"
    assert by["frag"].exists is False and by["frag"].status == "unconfirmed"
    assert by["missing"].exists is False and by["missing"].status == "ungrounded-unreachable"
    assert summ == {"grounding_total": 4, "grounding_verified": 1}

def test_verify_grounding_claims_leaves_citation_claims_untouched():
    """A claim with no grounding directive must be untouched (default Verification, not graded)."""
    from kp_build.verifier import verify_grounding_claims
    pkg = Package(topic="t", scope="s", papers=[Paper(cite_key="p1", title="T")],
                  claims=[Claim(id="c1", statement="s", paper="p1", supporting_passage="x")])
    summ = verify_grounding_claims(pkg, corpus={}, today="2026-01-01")
    assert summ == {"grounding_total": 0, "grounding_verified": 0}
    assert pkg.claims[0].verified.exists is False and pkg.claims[0].verified.status == "unverified"


# ── V2-b STEP 4: load_grounding_corpus — pack-local corpus/<source>.txt (offline) + DOI fallback ─

def test_load_grounding_corpus_reads_committed_file_offline(tmp_path):
    """The primary path: a committed corpus/<source>.txt is read OFFLINE, keyed by the directive's
    source. No `get` needed — a built pack re-grounds deterministically from a clean clone."""
    from kp_build.verifier import load_grounding_corpus
    (tmp_path / "corpus").mkdir()
    (tmp_path / "corpus" / "RFC9110.txt").write_text("The GET method requests transfer.", encoding="utf-8")
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="g", statement="s", paper="", supporting_passage="x",
              grounding={"source": "RFC9110", "supporting_passage": "The GET method requests transfer."})])
    corpus = load_grounding_corpus(pkg, tmp_path)        # no get -> offline only
    assert corpus == {"RFC9110": "The GET method requests transfer."}

def test_load_grounding_corpus_doi_fallback_when_no_committed_file(tmp_path):
    """Fallback: a source with no committed file but naming a DOI paper is fetched via fetch_doc_corpus
    (the live DOI path), exercised here with a fake transport. Keyed by cite_key == source."""
    from kp_build.verifier import load_grounding_corpus
    import json as _j
    fake = _j.dumps({"message": {"title": ["A Paper"],
                                 "abstract": "We present a method that improves the widget by twelve percent."}})
    pkg = Package(topic="t", scope="s",
                  papers=[Paper(cite_key="smith2026", title="A Paper", doi="10.1/x")],
                  claims=[Claim(id="g", statement="s", paper="", supporting_passage="x",
                                grounding={"source": "smith2026",
                                           "supporting_passage": "improves the widget by twelve percent."})])
    corpus = load_grounding_corpus(pkg, tmp_path, get=lambda url: fake)
    assert "smith2026" in corpus and "twelve percent" in corpus["smith2026"]

def test_load_grounding_corpus_omits_unheld_source(tmp_path):
    """A source with neither a committed file nor a DOI paper is omitted -> verifier later stamps it
    ungrounded-unreachable (never invented)."""
    from kp_build.verifier import load_grounding_corpus
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="g", statement="s", paper="", supporting_passage="x",
              grounding={"source": "NOWHERE", "supporting_passage": "a full sentence not held anywhere here."})])
    assert load_grounding_corpus(pkg, tmp_path, get=lambda url: "") == {}

def test_load_grounding_corpus_rejects_symlink_escape(tmp_path):
    """Security belt: a corpus/<source>.txt that is a SYMLINK escaping corpus/ must be
    refused by the is_relative_to check — the last guard if _load's source validation is ever bypassed."""
    import os
    secret = tmp_path / "secret.txt"; secret.write_text("TOP SECRET — outside the pack", encoding="utf-8")
    (tmp_path / "corpus").mkdir()
    os.symlink(secret, tmp_path / "corpus" / "evil.txt")        # corpus/evil.txt -> ../secret.txt (escapes)
    from kp_build.verifier import load_grounding_corpus
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="g", statement="s", paper="", supporting_passage="x",
              grounding={"source": "evil", "supporting_passage": "any full sentence to attempt grounding here."})])
    assert "evil" not in load_grounding_corpus(pkg, tmp_path)   # symlink escaping corpus/ is omitted

def test_grounding_tristate_verdicts_all_drop_at_ship_gate():
    """End-to-end contract: only a verbatim-present passage ships; ungrounded-unreachable
    (source not held) and unconfirmed (passage too short) both drop via claim_ships, never laundered."""
    from kp_build.verifier import verify_grounding_claims
    from kp_build.schema import claim_ships
    sentence = "The GET method requests transfer of a current representation of the target resource."
    pkg = Package(topic="t", scope="s", papers=[], claims=[
        Claim(id="ok", statement="s", paper="", supporting_passage="x",
              grounding={"source": "SRC", "supporting_passage": sentence}),
        Claim(id="unreach", statement="s", paper="", supporting_passage="x",
              grounding={"source": "NOPE", "supporting_passage": sentence}),
        Claim(id="unconf", statement="s", paper="", supporting_passage="x",
              grounding={"source": "SRC", "supporting_passage": "GET only"})])     # < 24 chars -> unconfirmed
    verify_grounding_claims(pkg, corpus={"SRC": sentence}, today="2026-01-01")
    ships = {c.id: claim_ships(c, set()) for c in pkg.claims}
    assert ships == {"ok": True, "unreach": False, "unconf": False}


# ── V2-b STEP 5: _cmd_build wiring — --ground-verify gate + the silent-drop hard-error guard ──

_GSENT = "The GET method requests transfer of a current representation of the target resource."

def _gbuild(tmp_path, passages, corpus_text=_GSENT, **over):
    """Write a grounding-spine research.json + a committed corpus/SRC.txt next to it, return build args."""
    (tmp_path / "corpus").mkdir(exist_ok=True)
    (tmp_path / "corpus" / "SRC.txt").write_text(corpus_text, encoding="utf-8")
    rj = {"topic": "t", "scope": "s",
          "claims": [{"id": cid, "statement": f"stmt {cid}", "supporting_passage": "disp",
                      "grounding": {"source": "SRC", "supporting_passage": p}} for cid, p in passages]}
    (tmp_path / "r.json").write_text(json.dumps(rj))
    args = SimpleNamespace(input=str(tmp_path / "r.json"), out=str(tmp_path / "out"), built="2026-01-01",
                           no_verify=False, throttle=0.0, reuse_verification=False, ground=False,
                           ground_fulltext=False, execute=False, ground_verify=False,
                           name="", version="0.1.0", license="CC-BY-4.0")
    for k, v in over.items():
        setattr(args, k, v)
    return args

def _claims_shipped(tmp_path):
    import json as _j
    return _j.loads((tmp_path / "out" / "wikillm.json").read_text())["stats"]["claims"]

def test_build_hard_errors_on_grounding_claims_without_ground_verify(tmp_path, capsys):
    """The silent-drop guard (critic #2): a grounding-directive claim built WITHOUT --ground-verify (and
    not --no-verify) must HARD-ERROR, never fall through the ship gate and silently vanish."""
    from kp_build.cli import _cmd_build
    assert _cmd_build(_gbuild(tmp_path, [("g1", _GSENT)])) == 2
    assert "ground-verify" in capsys.readouterr().err


def _jbuild(tmp_path, claims, **over):
    """Write a judgment-spine research.json, return build args (the judgment step runs by default — it's
    a deterministic replay of the recorded panel, no flag/IO)."""
    (tmp_path / "r.json").write_text(json.dumps({"topic": "t", "scope": "s", "claims": claims}))
    args = SimpleNamespace(input=str(tmp_path / "r.json"), out=str(tmp_path / "out"), built="2026-01-01",
                           no_verify=False, throttle=0.0, reuse_verification=False, ground=False,
                           ground_fulltext=False, execute=False, ground_verify=False,
                           name="", version="0.1.0", license="CC-BY-4.0")
    for k, v in over.items():
        setattr(args, k, v)
    return args

def _jclaim(cid, rounds):
    return {"id": cid, "statement": cid, "supporting_passage": "d",
            "judgment": {"task": "t", "answer": "A", "baseline": "B", "rounds": rounds}}

def test_build_judgment_pack_ships_only_genuine_winners(tmp_path):
    """End-to-end (no flag — deterministic replay): a genuine answer-winning recorded panel ships; a
    FAKED uniform panel (-> tie via the JudgeVerifier alternation) and a baseline-winning panel DROP."""
    from kp_build.cli import _cmd_build
    args = _jbuild(tmp_path, [_jclaim("win", ["a", "b", "a", "b"]),
                              _jclaim("fake", ["a", "a", "a", "a"]),
                              _jclaim("lose", ["b", "a", "b", "a"])])
    assert _cmd_build(args) == 0
    assert (tmp_path / "out" / "claims" / "win.md").exists()
    assert not (tmp_path / "out" / "claims" / "fake.md").exists()    # author can't fake a 'judged-better'
    assert not (tmp_path / "out" / "claims" / "lose.md").exists()
    assert _claims_shipped(tmp_path) == 1

def test_build_judgment_context_is_judgment_aware(tmp_path):
    """A judgment pack's CONTEXT must frame its claims as RELATIVE preference verdicts, not facts."""
    from kp_build.cli import _cmd_build
    assert _cmd_build(_jbuild(tmp_path, [_jclaim("win", ["a", "b", "a", "b"])])) == 0
    ctx = (tmp_path / "out" / "CONTEXT.md").read_text().lower()
    assert ("blind-panel" in ctx or "preference judgments" in ctx) and "do not invent citations" in ctx

def test_build_grounds_and_ships_with_ground_verify(tmp_path):
    """Happy path: --ground-verify grounds the verbatim passage against the committed corpus -> ships."""
    from kp_build.cli import _cmd_build
    assert _cmd_build(_gbuild(tmp_path, [("g1", _GSENT)], ground_verify=True)) == 0
    assert (tmp_path / "out" / "claims" / "g1.md").exists()
    assert _claims_shipped(tmp_path) == 1

def test_build_ground_verify_drops_ungrounded_keeps_grounded(tmp_path):
    """The hard negative: a fabricated (non-verbatim) clause stamps ungrounded and is VETOED; the
    verbatim one ships. This is the demonstrand the new fixtures will stage."""
    from kp_build.cli import _cmd_build
    fab = "The TRACE method permanently deletes all server logs without any authentication."  # not in corpus
    assert _cmd_build(_gbuild(tmp_path, [("ok", _GSENT), ("bad", fab)], ground_verify=True)) == 0
    assert (tmp_path / "out" / "claims" / "ok.md").exists()
    assert not (tmp_path / "out" / "claims" / "bad.md").exists()
    assert _claims_shipped(tmp_path) == 1

def test_build_no_verify_stamps_grounding_claims_so_pack_isnt_empty(tmp_path):
    """--no-verify is the offline escape hatch: grounding claims are stamped (unchecked) and ship, so a
    grounding-spine pack doesn't silently ship empty."""
    from kp_build.cli import _cmd_build
    assert _cmd_build(_gbuild(tmp_path, [("g1", _GSENT)], no_verify=True)) == 0
    assert _claims_shipped(tmp_path) == 1

def test_no_verify_does_not_overclaim_grounding_as_verified(tmp_path):
    """--no-verify ships grounding claims so the pack isn't empty, but MUST NOT stamp or
    print 'verified' / 'confirmed verbatim' on a clause nothing checked — least of all the fabricated one.
    The artifacts must read as UNCHECKED, the project's anti-overclaim brand."""
    from kp_build.cli import _cmd_build
    fab = "The TRACE method permanently deletes all server logs without any authentication."
    assert _cmd_build(_gbuild(tmp_path, [("ok", _GSENT), ("bad", fab)], no_verify=True)) == 0
    bad = (tmp_path / "out" / "claims" / "bad.md").read_text().lower()
    assert "grounding verified" not in bad            # no 'verified' tail on an unchecked (here fabricated) clause
    assert "status: verified" not in bad
    assert "status: unverified" in bad
    ctx = (tmp_path / "out" / "CONTEXT.md").read_text().lower()
    assert "confirmed verbatim" not in ctx            # the basis must not claim confirmation under --no-verify
    assert "not checked this build" in ctx

def test_ground_verify_still_says_confirmed_verbatim(tmp_path):
    """No regression: a REAL --ground-verify build keeps the 'confirmed verbatim' basis + 'grounding
    verified' tail (the shipped fixtures depend on this for their byte-identical CONTEXT)."""
    from kp_build.cli import _cmd_build
    assert _cmd_build(_gbuild(tmp_path, [("ok", _GSENT)], ground_verify=True)) == 0
    assert "confirmed verbatim" in (tmp_path / "out" / "CONTEXT.md").read_text().lower()
    assert "grounding verified" in (tmp_path / "out" / "claims" / "ok.md").read_text().lower()


def test_assemble_persists_relations_and_goal_metrics(tmp_path):
    from kp_build.schema import GoalMetric, Relation
    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    pkg = Package(topic="t", scope="s",
                  papers=[Paper(cite_key="p1", title="T", verified=v)],
                  claims=[Claim(id="c1", statement="a", paper="p1", supporting_passage="x"),
                          Claim(id="c2", statement="b", paper="p1", supporting_passage="y")],
                  goals={"g": "do thing"},
                  goal_metrics=[GoalMetric(name="strength", direction="higher", oracle_kind="grounding")],
                  relations=[Relation(id="r1", source="c1", target="c2", type="tradeoff",
                                      kpis=["strength", "water"],
                                      verification=Verification(exists=True, status="verified",
                                                                kind="grounding", evidence="q"))])
    out = assemble(pkg, tmp_path, built="2026-01-01")
    assert (out / "relations" / "r1.md").exists()
    man = json.loads((out / "wikillm.json").read_text())
    assert man["goals"]["g"] == "do thing"
    assert any(gm["name"] == "strength" for gm in man["goal_metrics"])
    assert man["stats"]["relations"] == 1


def test_context_has_goals_and_connections_when_present(tmp_path):
    from kp_build.schema import GoalMetric, Relation
    from kp_build.digest import build_context
    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    pkg = Package(topic="t", scope="s",
                  papers=[Paper(cite_key="p1", title="T", verified=v)],
                  claims=[Claim(id="c1", statement="a", paper="p1", supporting_passage="x"),
                          Claim(id="c2", statement="b", paper="p1", supporting_passage="y")],
                  goals={"g": "do the thing"},
                  goal_metrics=[GoalMetric(name="strength", direction="higher")],
                  relations=[Relation(id="r1", source="c1", target="c2", type="tradeoff",
                                      kpis=["strength", "water"], description="trade")])
    ctx = build_context(pkg, built="2026-01-01")
    assert "Goals" in ctx and "strength" in ctx
    assert "onnection" in ctx and "tradeoff" in ctx


def test_context_preamble_is_verifier_aware_for_paperless_pack():
    """An execution pack has no citation spine; CONTEXT.md (the agent payload) must NOT tell the
    loading agent the spine was 'verified to exist by arXiv id / DOI' — that boilerplate misframes a
    zero-citation pack as citation-grounded. It should name the real basis (execution) and still
    forbid inventing citations. A citation pack must keep the arXiv/DOI sentence (no regression)."""
    from kp_build.digest import build_context
    exec_pkg = Package(topic="t", scope="s", papers=[],
                       claims=[Claim(id="c1", statement="a", paper="", supporting_passage="",
                                     execution={"tool": "lint", "gate_code": "x", "artifact": "a/b"})])
    ctx = build_context(exec_pkg, built="2026-01-01")
    assert "verified to exist by arXiv id / DOI" not in ctx   # no citation boilerplate on a paperless pack
    assert "do not invent citations" in ctx                    # guardrail retained
    assert "execution" in ctx.lower()                          # names the real basis

    grnd_pkg = Package(topic="t", scope="s", papers=[],
                       claims=[Claim(id="g", statement="a", paper="", supporting_passage="",
                                     grounding={"source": "RFC9110", "supporting_passage": "q"})])
    gctx = build_context(grnd_pkg, built="2026-01-01")
    assert "verified to exist by arXiv id / DOI" not in gctx
    assert "do not invent citations" in gctx
    assert "grounding" in gctx.lower()                         # names doc-grounding, not the vague fallback

    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    cit_pkg = Package(topic="t", scope="s", papers=[Paper(cite_key="p1", title="T", verified=v)],
                      claims=[Claim(id="c1", statement="a", paper="p1", supporting_passage="x")])
    assert "verified to exist by arXiv id / DOI" in build_context(cit_pkg, built="2026-01-01")


# ── v2-b: JudgeVerifier — the RELATIVE, order-unbiased aesthetic/quality judge (the 4th verifier) ──

def test_judge_verifier_prefers_better_answer_and_satisfies_protocol():
    """JudgeVerifier (kind='judgment') judges an answer AGAINST a baseline via an injected blind judge.
    A judge that prefers the answer's content -> judged-better -> exists=True (it 'ships' as helpful)."""
    from kp_build.verifier import JudgeVerifier, Verifier
    from types import SimpleNamespace
    judge = lambda task, a, b: {"winner": "a" if "PACK" in a else "b"}   # prefers the 'PACK' content
    v = JudgeVerifier(judge, rounds=4).verify(SimpleNamespace(task="t", answer="PACK answer", baseline="base"))
    assert v.kind == "judgment" and v.exists is True and v.status == "judged-better"
    assert isinstance(JudgeVerifier(judge), Verifier)            # satisfies the Verifier protocol

def test_judge_verifier_baseline_wins():
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    judge = lambda task, a, b: {"winner": "a" if "BASE" in a else "b"}
    v = JudgeVerifier(judge, rounds=4).verify(SimpleNamespace(task="t", answer="pack", baseline="BASE ans"))
    assert v.exists is False and v.status == "judged-worse"

def test_judge_verifier_position_bias_nets_to_tie():
    """A purely position-biased judge (always picks slot 'a') must NET TO A TIE, because the verifier
    alternates which answer occupies slot a/b across rounds. This is the anti-tautology guarantee."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    v = JudgeVerifier(lambda task, a, b: {"winner": "a"}, rounds=4).verify(
        SimpleNamespace(task="t", answer="pack", baseline="base"))
    assert v.status == "judged-tie" and v.exists is False

def test_judge_verifier_requires_a_baseline_relative_only():
    """No absolute taste gate: with no baseline the verdict is 'unverifiable', never a guessed pass."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    v = JudgeVerifier(lambda task, a, b: {"winner": "a"}).verify(SimpleNamespace(task="t", answer="x", baseline=""))
    assert v.exists is False and v.status == "unverifiable"

def test_judge_verifier_never_trusts_a_failed_judge():
    """A judge that raises (or returns junk) contributes NO vote — never fail-open to 'better'."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    def boom(task, a, b): raise RuntimeError("judge down")
    v = JudgeVerifier(boom, rounds=4).verify(SimpleNamespace(task="t", answer="pack", baseline="base"))
    assert v.exists is False and v.status == "judged-tie"       # 0-0, no votes -> tie, not better

def test_judge_verifier_rounds_forced_even_protects_alternation():
    """The rounds count is normalized to even (>=2). An ODD requested count must NOT let a
    position-biased judge win — this is the single line the whole anti-tautology guarantee rests on."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    assert JudgeVerifier(lambda *a: {}, rounds=3)._rounds == 2
    assert JudgeVerifier(lambda *a: {}, rounds=5)._rounds == 4
    assert JudgeVerifier(lambda *a: {}, rounds=1)._rounds == 2
    # a purely position-biased judge driven at an odd requested count still nets to a tie
    v = JudgeVerifier(lambda task, a, b: {"winner": "a"}, rounds=5).verify(
        SimpleNamespace(task="t", answer="pack", baseline="base"))
    assert v.status == "judged-tie" and v.exists is False

@pytest.mark.parametrize("bad", [None, {}, {"winner": "banana"}, "a", ["a"], {"winner": "A"}])
def test_judge_verifier_malformed_judge_output_is_no_vote(bad):
    """A judge that returns junk (not just one that raises) contributes NO vote.
    The bare-string 'a' is the most likely real LLM-wrapper bug; none may ever produce a win."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    v = JudgeVerifier(lambda task, a, b: bad, rounds=4).verify(SimpleNamespace(task="t", answer="x", baseline="y"))
    assert v.exists is False and v.status == "judged-tie"

def test_judge_verifier_empty_answer_is_unverifiable_not_a_win():
    """A relative judge needs BOTH sides — an empty answer must never be able to
    'win' against a baseline (a latent fail-open), it is unverifiable like an empty baseline."""
    from kp_build.verifier import JudgeVerifier
    from types import SimpleNamespace
    v = JudgeVerifier(lambda task, a, b: {"winner": "a" if a == "" else "b"}, rounds=4).verify(
        SimpleNamespace(task="t", answer="", baseline="base"))
    assert v.exists is False and v.status == "unverifiable"


# ── verifier.py: the pluggable seam — CitationVerifier == legacy (RED until implemented) ──────

def test_citation_verifier_equals_legacy_and_satisfies_protocol():
    """The seam exists in code: CitationVerifier wraps citations.verify_paper and is byte-identical to
    the legacy path (a narrow lift), and it satisfies the Verifier protocol with kind='existence'."""
    from kp_build.verifier import CitationVerifier, Verifier
    from kp_build import citations
    g = lambda url: ""                       # offline: no hit -> both paths agree deterministically
    kw = dict(today="2026-01-01", sleep=lambda _: None, max_retries=0)
    legacy = citations.verify_paper(Paper(cite_key="x", title="T", arxiv_id="1706.03762"), get=g, **kw).verified
    v = CitationVerifier(get=g, **kw).verify(Paper(cite_key="x", title="T", arxiv_id="1706.03762"))
    assert v == legacy                       # verifier-equals-legacy (the characterization)
    assert v.kind == "existence"
    assert isinstance(CitationVerifier(), Verifier)      # the protocol is satisfied


# ── verifier.py: DocGroundingVerifier — offline passage grounding (RED until implemented) ─────

def test_doc_grounding_verifier_grounds_passage_present_in_corpus():
    """A claim whose passage really appears in the pinned source text grounds verified (kind='grounding'),
    with NO network — the corpus is injected at construction (the §4.4 offline path)."""
    from kp_build.verifier import DocGroundingVerifier
    text = ("Polyamide 6 absorbs substantial water, with average saturation around 8.83 percent "
            "in an 80 C bath, which plasticizes the polymer and lowers its modulus.")
    claim = Claim(id="c8", statement="nylon absorbs water", paper="sambale2021",
                  supporting_passage="average saturation around 8.83 percent in an 80 C bath")
    v = DocGroundingVerifier({"sambale2021": text}).verify(claim)
    assert v.kind == "grounding" and v.exists is True and v.status == "verified"
    assert v.evidence.startswith("average saturation")


def test_doc_grounding_verifier_flags_absent_passage_as_ungrounded():
    from kp_build.verifier import DocGroundingVerifier
    claim = Claim(id="c", statement="s", paper="p",
                  supporting_passage="zylophone quasar nimbus fjord glyph wexford plinth bramble")
    v = DocGroundingVerifier({"p": "polyamide six absorbs water and plasticizes when wet here."}).verify(claim)
    assert v.exists is False and v.status == "ungrounded"


def test_doc_grounding_verifier_unreachable_when_source_absent_from_corpus():
    """Source not in the pinned corpus = a COVERAGE DEBT (ungrounded-unreachable), NOT a permanent
    ceiling and NOT laundered into verified — couldn't-check and checked-and-absent carry distinct stamps."""
    from kp_build.verifier import DocGroundingVerifier
    claim = Claim(id="c", statement="s", paper="missing_paper",
                  supporting_passage="some passage long enough to actually check against a source text")
    v = DocGroundingVerifier({}).verify(claim)
    assert v.exists is False and v.status == "ungrounded-unreachable"


def test_doc_grounding_verifier_offline_and_satisfies_protocol():
    from kp_build.verifier import DocGroundingVerifier, Verifier
    assert isinstance(DocGroundingVerifier({}), Verifier)
    assert DocGroundingVerifier({}).kind == "grounding"


# ── ground.fetch_doc_corpus — minimal Crossref-abstract corpus builder (RED until implemented) ──

def test_fetch_doc_corpus_extracts_and_cleans_crossref_abstract():
    from kp_build.ground import fetch_doc_corpus
    crossref = json.dumps({"message": {"title": ["Sorption of Water in Polyamide 6"],
        "abstract": "<jats:p>Polyamide 6 absorbs substantial water, with saturation around "
                    "8.83 percent in an 80 C bath.</jats:p>"}})
    corpus = fetch_doc_corpus([Paper(cite_key="p1", title="t", doi="10.3390/polym13091480")],
                              get=lambda url: crossref)
    assert "p1" in corpus
    assert "8.83 percent" in corpus["p1"] and "<jats" not in corpus["p1"]   # JATS tags stripped


def test_fetch_doc_corpus_skips_no_doi_and_no_abstract():
    from kp_build.ground import fetch_doc_corpus
    assert fetch_doc_corpus([Paper(cite_key="p1", title="t", doi="")], get=lambda u: "x") == {}
    title_only = json.dumps({"message": {"title": ["No abstract here"]}})
    assert "p2" not in fetch_doc_corpus([Paper(cite_key="p2", title="t", doi="10.x/y")],
                                        get=lambda u: title_only)


def test_doc_grounding_verifier_grounds_against_fetched_corpus_end_to_end():
    """The two halves compose: fetch a corpus, then ground a claim's passage against it."""
    from kp_build.ground import fetch_doc_corpus
    from kp_build.verifier import DocGroundingVerifier
    crossref = json.dumps({"message": {"title": ["T"],
        "abstract": "<jats:p>average saturation around 8.83 percent in an 80 C bath</jats:p>"}})
    corpus = fetch_doc_corpus([Paper(cite_key="p1", title="t", doi="10.x/y")], get=lambda u: crossref)
    claim = Claim(id="c8", statement="s", paper="p1",
                  supporting_passage="average saturation around 8.83 percent in an 80 C bath")
    assert DocGroundingVerifier(corpus).verify(claim).status == "verified"


# ── verifier.py: ExecutionVerifier — runs a gate via an injected runner (RED until implemented) ──

from types import SimpleNamespace

def _directive(artifact="fixed/", tool="lint", gate_code="non_deterministic_code", aesthetic=False):
    return SimpleNamespace(artifact=artifact, tool=tool, gate_code=gate_code, aesthetic=aesthetic)


def test_execution_verifier_verified_when_gate_clears():
    """Ran clean and the asserted gate is ABSENT -> the mechanical fundamental holds."""
    from kp_build.verifier import ExecutionVerifier
    v = ExecutionVerifier(lambda artifact, tool: {"codes": []}).verify(_directive())
    assert v.kind == "execution" and v.exists is True and v.status == "verified"


def test_execution_verifier_clean_run_wrong_output_is_output_mismatch():
    """Ran clean but the gate FIRED -> the artifact violates what it claims (the new status)."""
    from kp_build.verifier import ExecutionVerifier
    v = ExecutionVerifier(lambda a, t: {"codes": ["non_deterministic_code"]}).verify(_directive())
    assert v.exists is False and v.status == "output-mismatch"


def test_execution_verifier_not_found_when_runner_returns_none():
    from kp_build.verifier import ExecutionVerifier
    v = ExecutionVerifier(lambda a, t: None).verify(_directive())
    assert v.exists is False and v.status == "not-found"


def test_execution_verifier_error_on_runner_failure_is_never_trusted():
    from kp_build.verifier import ExecutionVerifier
    def boom(a, t): raise TimeoutError("sandbox timeout")
    v = ExecutionVerifier(boom).verify(_directive())
    assert v.exists is False and v.status == "error"


def test_execution_verifier_refuses_aesthetic_claims_as_unverifiable():
    """A claim with no mechanical oracle returns unverifiable — it NEVER guesses pass for taste."""
    from kp_build.verifier import ExecutionVerifier
    ran = []
    def runner(a, t): ran.append(1); return {"codes": []}
    v = ExecutionVerifier(runner).verify(_directive(aesthetic=True, gate_code=""))
    assert v.exists is False and v.status == "unverifiable"
    assert ran == []                              # never even runs the tool for a taste claim


def test_execution_verifier_offline_and_satisfies_protocol():
    from kp_build.verifier import ExecutionVerifier, Verifier
    assert isinstance(ExecutionVerifier(lambda a, t: {"codes": []}), Verifier)
    assert ExecutionVerifier(lambda a, t: {}).kind == "execution"


# ── ship-gate generalization: a claim ships via its PAPER *or* its own verdict (RED until done) ──

def test_ship_gate_ships_execution_claim_via_per_claim_verdict(tmp_path: Path):
    """An execution claim has NO citation paper — it ships on its own verifier verdict (exists=True),
    and a rejected one (output-mismatch) is dropped. Academic, paper-anchored claims are unaffected."""
    pkg = Package(
        topic="hf", scope="composition fundamentals",
        claims=[
            Claim(id="hf1", statement="never call Math.random()", paper="", supporting_passage="...",
                  verified=Verification(kind="execution", exists=True, status="verified",
                                        via="hyperframes-cli@0.6.91", evidence="lint:non_deterministic_code cleared")),
            Claim(id="hf2", statement="a violating fundamental", paper="", supporting_passage="...",
                  verified=Verification(kind="execution", exists=False, status="output-mismatch",
                                        via="hyperframes-cli@0.6.91", evidence="lint:non_deterministic_code fired")),
        ],
    )
    out = assemble(pkg, tmp_path, built="2026-01-01")
    assert (out / "claims" / "hf1.md").exists()          # self-verified execution claim ships
    assert not (out / "claims" / "hf2.md").exists()       # output-mismatch claim dropped


def test_claim_round_trips_with_per_claim_execution_verdict():
    from kp_build.schema import claim_to_md, claim_from_md
    c = Claim(id="hf1", statement="never call Math.random()", paper="", supporting_passage="seed your PRNG",
              verified=Verification(kind="execution", exists=True, status="verified",
                                    via="hyperframes-cli@0.6.91", evidence="lint:non_deterministic_code cleared"))
    back = claim_from_md(claim_to_md(c))
    assert back == c
    assert back.verified.kind == "execution" and back.verified.exists is True


# ── wire ExecutionVerifier into build: execution directive + verify_execution_claims (RED) ───────

def test_load_parses_execution_directive_and_relaxes_paper_requirement(tmp_path):
    from kp_build.cli import _load
    rj = {"topic": "hf", "scope": "s", "claims": [
        {"id": "e1", "statement": "no Math.random", "supporting_passage": "seed your prng",
         "execution": {"tool": "lint", "gate_code": "non_deterministic_code", "artifact": "fixed/"}}]}
    pkg = _load(_write(tmp_path, rj))
    assert pkg.claims[0].execution["tool"] == "lint"
    assert pkg.claims[0].execution["gate_code"] == "non_deterministic_code"
    assert pkg.claims[0].paper == ""                  # an execution claim needs no citation paper


def test_load_rejects_claim_with_neither_paper_nor_execution(tmp_path):
    from kp_build.cli import _load, ResearchInputError
    rj = {"topic": "t", "claims": [{"id": "x", "statement": "s", "supporting_passage": "p"}]}
    with pytest.raises(ResearchInputError, match="needs a 'paper', an 'execution', a 'grounding', or a 'judgment'"):
        _load(_write(tmp_path, rj))


def test_claim_round_trips_with_execution_directive():
    from kp_build.schema import claim_to_md, claim_from_md
    c = Claim(id="e1", statement="s", paper="", supporting_passage="p",
              execution={"tool": "lint", "gate_code": "nd", "artifact": "a"})
    assert claim_from_md(claim_to_md(c)).execution == {"tool": "lint", "gate_code": "nd", "artifact": "a"}


def test_verify_execution_claims_sets_verdicts_and_ships(tmp_path: Path):
    """The build step: run the ExecutionVerifier (injected runner) on execution claims → set per-claim
    verdict → assemble ships the passing one and drops the output-mismatch one."""
    from kp_build.verifier import verify_execution_claims
    pkg = Package(topic="hf", scope="s", claims=[
        Claim(id="e1", statement="ok", paper="", supporting_passage="x",
              execution={"tool": "lint", "gate_code": "nd", "artifact": "a"}),
        Claim(id="e2", statement="bad", paper="", supporting_passage="y",
              execution={"tool": "lint", "gate_code": "nd", "artifact": "b"}),
    ])
    fake = lambda artifact, tool: {"codes": [] if artifact == "a" else ["nd"]}   # a clean, b fires the gate
    summary = verify_execution_claims(pkg, runner=fake, today="2026-01-01")
    assert summary == {"execution_total": 2, "execution_verified": 1}
    assert pkg.claims[0].verified.status == "verified" and pkg.claims[0].verified.exists is True
    assert pkg.claims[1].verified.status == "output-mismatch" and pkg.claims[1].verified.exists is False
    out = assemble(pkg, tmp_path, built="2026-01-01")
    assert (out / "claims" / "e1.md").exists() and not (out / "claims" / "e2.md").exists()


# ── hardening: filename-safe ids, mechanical veto, one verification basis, sanitized context ─

def test_load_rejects_path_unsafe_node_ids(tmp_path):
    """Every node id (not just cite_key) is used as a filename — a '/'/'..'/absolute id is an
    arbitrary-file-write. _load must reject them like it does cite_keys."""
    from kp_build.cli import _load, ResearchInputError
    for bad in ["../../../tmp/PWNED", "a/b", "/abs", ".."]:
        rj = {"topic": "t", "papers": [{"cite_key": "p1", "title": "T"}],
              "claims": [{"id": bad, "statement": "s", "paper": "p1", "supporting_passage": "x"}]}
        with pytest.raises(ResearchInputError, match="unsafe|invalid"):
            _load(_write(tmp_path, rj))


def test_paper_claim_with_firing_execution_gate_is_dropped(tmp_path: Path):
    """A mechanical disproof must VETO a citation anchor. A claim with a verified paper AND a
    firing execution gate (output-mismatch) must NOT ship."""
    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    pkg = Package(topic="t", scope="s",
                  papers=[Paper(cite_key="p1", title="T", verified=v)],
                  claims=[Claim(id="c1", statement="disproven", paper="p1", supporting_passage="x",
                                execution={"tool": "lint", "gate_code": "nd", "artifact": "a.html"},
                                verified=Verification(kind="execution", exists=False, status="output-mismatch",
                                                      via="hf", evidence="lint:nd fired"))])
    out = assemble(pkg, tmp_path, built="2026-01-01")
    assert not (out / "claims" / "c1.md").exists()        # the firing gate vetoes the citation


def test_load_rejects_claim_with_both_paper_and_execution(tmp_path):
    """Belt to the disproof-veto: one verified unit per node — paper XOR execution XOR grounding, never more than one."""
    from kp_build.cli import _load, ResearchInputError
    rj = {"topic": "t", "papers": [{"cite_key": "p1", "title": "T"}],
          "claims": [{"id": "c1", "statement": "s", "paper": "p1", "supporting_passage": "x",
                      "execution": {"tool": "lint", "gate_code": "nd", "artifact": "a.html"}}]}
    with pytest.raises(ResearchInputError, match="more than one verification basis"):
        _load(_write(tmp_path, rj))


def test_context_sanitizes_relation_and_goal_fields():
    """The V2-a relation/goal fields are attacker-controlled and must be _data-sanitized
    before landing in the agent-loaded CONTEXT.md (no prompt-injection bypass)."""
    from kp_build.schema import GoalMetric, Relation
    from kp_build.digest import build_context
    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    pkg = Package(topic="t", scope="s",
                  papers=[Paper(cite_key="p1", title="T", verified=v)],
                  claims=[Claim(id="c1", statement="a", paper="p1", supporting_passage="x"),
                          Claim(id="c2", statement="b", paper="p1", supporting_passage="y")],
                  goal_metrics=[GoalMetric(name="m", direction="higher", oracle_kind="exec```pwn")],
                  relations=[Relation(id="r1", source="c1", target="c2", type="trade```evil",
                                      kpis=["k```bad"], description="d")])
    ctx = build_context(pkg, built="2026-01-01")
    assert "```" not in ctx                               # every rendered field sanitized


@pytest.fixture(autouse=True)
def _hyperframes_pin_isolated(monkeypatch):
    """The supply-chain pin is per-PROCESS state — without isolation one test's confirmed check would
    leak into the next. Default each test to 'pin already confirmed' (parse/extraction tests exercise
    parsing, not the registry check) and a clean env; the pin tests reset the flag to False themselves."""
    import kp_build.verifier as _verifier
    monkeypatch.setattr(_verifier, "_hyperframes_integrity_ok", True)
    monkeypatch.delenv("KP_BUILD_HYPERFRAMES_BIN", raising=False)


def test_hyperframes_runner_extracts_codes_per_tool():
    """Pin the PRODUCTION default runner's per-tool parse/extraction via an injected run fn."""
    from kp_build.verifier import hyperframes_runner
    from types import SimpleNamespace
    def run(out):
        return lambda *a, **k: SimpleNamespace(stdout=out)
    assert hyperframes_runner("x", "lint", _run=run('{"findings":[{"code":"nd"},{"code":"rep"}]}')) == {"codes": ["nd", "rep"]}
    assert hyperframes_runner("x", "inspect", _run=run('{"issues":[{"code":"overflow"}]}')) == {"codes": ["overflow"]}
    assert hyperframes_runner("x", "validate", _run=run('{"contrastFailures":3}')) == {"codes": ["contrastFailures"]}
    assert hyperframes_runner("x", "validate", _run=run('{"contrastFailures":0}')) == {"codes": []}
    # a CRASHED inspect (ok:false / error set — e.g. root composition missing data-duration) must surface
    # an 'inspect_error' sentinel, NOT read as clean (issues:[] -> codes:[] would false-verify any claim)
    assert hyperframes_runner("x", "inspect", _run=run('{"ok":false,"error":"reading totalDuration","issues":[]}')) == {"codes": ["inspect_error"]}
    assert hyperframes_runner("x", "inspect", _run=run('{"ok":true,"issues":[]}')) == {"codes": []}


def test_execution_verifier_inspect_error_sentinel_fails_any_claim():
    """The crashed-inspect false-positive (found patching the root-data-duration gap): if inspect could
    not run, NO inspect-gated claim may verify — even one whose specific gate_code is absent."""
    from kp_build.verifier import ExecutionVerifier
    from types import SimpleNamespace
    v = ExecutionVerifier(lambda art, tool: {"codes": ["inspect_error"]}).verify(
        SimpleNamespace(tool="inspect", gate_code="text_box_overflow", artifact="x"))
    assert v.exists is False and v.status == "output-mismatch"
    # the evidence must say inspect could not run, NOT that text_box_overflow 'fired'
    assert "could not run" in v.evidence and "text_box_overflow fired" not in v.evidence

def test_hyperframes_runner_staticguard_invalid_contract_is_inspect_error():
    """A contract-INVALID composition prints '[StaticGuard] Invalid HyperFrame
    contract' to stderr but {ok:true, issues:[]} on stdout — the runner must NOT read that as clean."""
    from kp_build.verifier import hyperframes_runner
    from types import SimpleNamespace
    run = lambda out, err="": (lambda *a, **k: SimpleNamespace(stdout=out, stderr=err))
    bad = run('{"ok":true,"issues":[]}', err="[StaticGuard] Invalid HyperFrame contract: missing data-width")
    assert hyperframes_runner("x", "inspect", _run=bad) == {"codes": ["inspect_error"]}
    # a valid clean inspect (no StaticGuard) is still clean
    assert hyperframes_runner("x", "inspect", _run=run('{"ok":true,"issues":[]}', err="")) == {"codes": []}


def test_hyperframes_runner_none_on_no_json_bad_json_or_unknown_tool():
    from kp_build.verifier import hyperframes_runner
    from types import SimpleNamespace
    run = lambda out: (lambda *a, **k: SimpleNamespace(stdout=out))
    assert hyperframes_runner("x", "lint", _run=run("error: no brace here")) is None     # no JSON
    assert hyperframes_runner("x", "lint", _run=run("{not valid json")) is None           # malformed -> None, no crash
    assert hyperframes_runner("x", "render", _run=run('{"findings":[]}')) is None          # unknown tool


def test_validate_rejects_no_paper_no_verdict_claim(tmp_path: Path):
    """validate must reject a shipped claim that carries neither a cited paper nor a verifier verdict."""
    from kp_build.validate import validate
    from kp_build.schema import claim_to_md
    for sub in ("papers", "claims", "open-problems", "debates", "benchmarks", "relations"):
        (tmp_path / sub).mkdir()
    (tmp_path / "claims" / "bad.md").write_text(
        claim_to_md(Claim(id="bad", statement="s", paper="", supporting_passage="p")))
    res = validate(tmp_path)
    assert any("neither a cited paper nor a verifier verdict" in e for e in res.errors)


def test_fetch_doc_corpus_survives_network_error_and_bad_json():
    """A network error or bad JSON while fetching the corpus yields an empty corpus, never a crash."""
    from kp_build.ground import fetch_doc_corpus
    def err(url): raise RuntimeError("network down")
    assert fetch_doc_corpus([Paper(cite_key="p1", title="t", doi="10.x/y")], get=err) == {}
    assert fetch_doc_corpus([Paper(cite_key="p1", title="t", doi="10.x/y")], get=lambda u: "not json") == {}


def test_doc_grounding_verifier_unconfirmed_on_too_short_passage():
    """A passage too short to check lands in the `unconfirmed`(None) honesty branch — abstain, not a verdict."""
    from kp_build.verifier import DocGroundingVerifier
    v = DocGroundingVerifier({"p1": "a much longer source text that does not contain that exact phrase here."}).verify(
        Claim(id="c", statement="s", paper="p1", supporting_passage="too short"))
    assert v.status == "unconfirmed" and v.exists is False and v.kind == "grounding"


def test_execution_verifier_non_list_codes_is_not_silently_verified():
    """A malformed runner result {'codes':'nd'} must NOT fail-OPEN to verified via substring."""
    from kp_build.verifier import ExecutionVerifier
    v = ExecutionVerifier(lambda a, t: {"codes": "non_deterministic_code"}).verify(_directive())
    assert v.status == "error" and v.exists is False     # non-list codes -> untrusted, never verified


def test_index_labels_unverified_relations_honestly(tmp_path: Path):
    """Relations ship UNVERIFIED (no relation-grounding step); the index must not print a
    misleading 'verified': false — it labels them 'unrun'."""
    import json as _json
    from kp_build.schema import Relation
    v = Verification(exists=True, status="verified", via="arxiv", canonical_title="T", checked="2026-01-01")
    pkg = Package(topic="t", scope="s", papers=[Paper(cite_key="p1", title="T", verified=v)],
                  claims=[Claim(id="c1", statement="a", paper="p1", supporting_passage="x"),
                          Claim(id="c2", statement="b", paper="p1", supporting_passage="y")],
                  relations=[Relation(id="r1", source="c1", target="c2", type="tradeoff", kpis=["a", "b"])])
    out = assemble(pkg, tmp_path, built="2026-01-01")
    idx = _json.loads((out / "index.json").read_text())
    assert idx["relations"][0]["verification"] == "unrun"
    assert "verified" not in idx["relations"][0]          # no misleading boolean


def test_load_rejects_unsafe_execution_artifact(tmp_path):
    """The execution artifact is fed to a subprocess that reads files — reject absolute paths,
    '..' traversal, and URL schemes (arbitrary local-file read / SSRF)."""
    from kp_build.cli import _load, ResearchInputError
    for bad in ["/etc/passwd", "../../../etc/passwd", "http://evil/x", "a/../b"]:
        rj = {"topic": "t", "claims": [{"id": "e1", "statement": "s", "supporting_passage": "p",
              "execution": {"tool": "lint", "gate_code": "nd", "artifact": bad}}]}
        with pytest.raises(ResearchInputError, match="artifact"):
            _load(_write(tmp_path, rj))


def test_load_accepts_relative_execution_artifact(tmp_path):
    from kp_build.cli import _load
    rj = {"topic": "t", "claims": [{"id": "e1", "statement": "s", "supporting_passage": "p",
          "execution": {"tool": "lint", "gate_code": "nd", "artifact": "fixtures/det-1/fixed"}}]}
    assert _load(_write(tmp_path, rj)).claims[0].execution["artifact"] == "fixtures/det-1/fixed"


def test_validate_accepts_no_paper_execution_claim(tmp_path: Path):
    """A shipped execution claim has paper='' — validate must accept it (it carries its own verdict),
    not flag 'cites unknown paper'."""
    from kp_build.validate import validate
    pkg = Package(topic="hf", scope="s", claims=[
        Claim(id="e1", statement="ok", paper="", supporting_passage="x",
              verified=Verification(kind="execution", exists=True, status="verified",
                                    via="hyperframes-cli@0.6.91", evidence="lint:nd cleared"))])
    res = validate(assemble(pkg, tmp_path, built="2026-01-01"))
    assert not any("unknown paper" in e for e in res.errors)
    assert res.ok


# ── supply-chain: the TOFU integrity pin on the npx-fetched hyperframes CLI ──────────────────

def _pin_run(view_out, tool_out='{"findings":[{"code":"nd"}]}'):
    """A subprocess.run-shaped fake covering BOTH calls the runner makes: `npm view` (the integrity
    check) answers ``view_out``; the tool invocation answers ``tool_out``. Records every argv."""
    def run(cmd, **k):
        run.calls.append(list(cmd))
        return SimpleNamespace(stdout=(view_out if cmd[:2] == ["npm", "view"] else tool_out), stderr="")
    run.calls = []
    return run


def test_hyperframes_runner_pin_match_runs_tool_as_before(monkeypatch):
    """Registry still serves the recorded integrity -> the check passes, npx runs, and parse/extraction
    is byte-identical to the pre-pin behavior."""
    import kp_build.verifier as verifier
    from kp_build.verifier import hyperframes_runner, _HYPERFRAMES_INTEGRITY, _HYPERFRAMES_PKG
    monkeypatch.setattr(verifier, "_hyperframes_integrity_ok", False)
    run = _pin_run(_HYPERFRAMES_INTEGRITY + "\n", '{"findings":[{"code":"nd"},{"code":"rep"}]}')
    assert hyperframes_runner("x", "lint", _run=run) == {"codes": ["nd", "rep"]}
    assert run.calls[0] == ["npm", "view", _HYPERFRAMES_PKG, "dist.integrity"]
    assert run.calls[1] == ["npx", "--yes", _HYPERFRAMES_PKG, "lint", "--json", "x"]


def test_hyperframes_runner_pin_mismatch_raises_and_claim_lands_error(monkeypatch):
    """The attack: the registry serves a DIFFERENT artifact under the pinned version (post-pin hijack /
    re-publish). The runner raises BEFORE any npx fetch, and through ExecutionVerifier the claim lands
    status='error', exists=False — never verified."""
    import kp_build.verifier as verifier
    from kp_build.verifier import hyperframes_runner, ExecutionVerifier
    monkeypatch.setattr(verifier, "_hyperframes_integrity_ok", False)
    bad = _pin_run("sha512-EVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVILEVIL==")
    with pytest.raises(RuntimeError, match="different artifact"):
        hyperframes_runner("x", "lint", _run=bad)
    assert all(c[0] != "npx" for c in bad.calls)          # nothing fetched, nothing executed
    # a failed check is never cached — the verifier path re-checks and maps the raise to 'error'
    v = ExecutionVerifier(lambda a, t: hyperframes_runner(a, t, _run=bad)).verify(_directive())
    assert v.exists is False and v.status == "error"


def test_hyperframes_runner_pin_empty_or_garbage_output_raises(monkeypatch):
    """An empty or unparseable `npm view` answer is treated as a mismatch — the check never fails OPEN."""
    import kp_build.verifier as verifier
    from kp_build.verifier import hyperframes_runner
    for out in ("", "   \n", "npm ERR! code E404"):
        monkeypatch.setattr(verifier, "_hyperframes_integrity_ok", False)
        with pytest.raises(RuntimeError, match="different artifact"):
            hyperframes_runner("x", "lint", _run=_pin_run(out))


def test_hyperframes_runner_audited_bin_override_skips_registry_check(monkeypatch):
    """KP_BUILD_HYPERFRAMES_BIN = the operator's own audited install: run it directly — no npm fetch
    happens, so there is no registry to distrust and `npm view` is NEVER consulted."""
    import kp_build.verifier as verifier
    from kp_build.verifier import hyperframes_runner
    monkeypatch.setattr(verifier, "_hyperframes_integrity_ok", False)
    monkeypatch.setenv("KP_BUILD_HYPERFRAMES_BIN", "/opt/audited/hyperframes")
    run = _pin_run("sha512-WOULD-FAIL-IF-CONSULTED", '{"findings":[{"code":"nd"}]}')
    assert hyperframes_runner("art.html", "lint", _run=run) == {"codes": ["nd"]}
    assert run.calls == [["/opt/audited/hyperframes", "lint", "--json", "art.html"]]


def test_hyperframes_runner_pin_checked_once_per_process(monkeypatch):
    """A multi-gate build queries `npm view` ONCE — the confirmed pin is cached at module level."""
    import kp_build.verifier as verifier
    from kp_build.verifier import hyperframes_runner, _HYPERFRAMES_INTEGRITY
    monkeypatch.setattr(verifier, "_hyperframes_integrity_ok", False)
    run = _pin_run(_HYPERFRAMES_INTEGRITY, '{"findings":[]}')
    assert hyperframes_runner("x", "lint", _run=run) == {"codes": []}
    assert hyperframes_runner("x", "lint", _run=run) == {"codes": []}
    assert sum(1 for c in run.calls if c[:2] == ["npm", "view"]) == 1
    assert sum(1 for c in run.calls if c[0] == "npx") == 2
