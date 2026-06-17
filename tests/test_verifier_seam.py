"""V2-a: the pluggable verifier seam — §4.0 widen the Verification contract from citation-shaped
to verifier-agnostic, WITHOUT changing academic-pack behavior.

TDD regression net (design review S1/S4, Blocker 2):
- characterization tests lock the CURRENT academic ship-gate behavior (green on the pre-refactor code);
- the widened-contract tests are RED until §4.0 lands, then green — the academic ones must stay green.
"""
from pathlib import Path

from kp_build.schema import (
    Package, Paper, Claim, Verification, paper_to_md, paper_from_md,
)
from kp_build.assemble import assemble


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
    # the load-bearing invariant: a Claim has no per-claim verdict field
    assert not hasattr(pkg.claims[0], "verified")


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
    ceiling and NOT laundered into verified (the review's two-stamp scheme)."""
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
