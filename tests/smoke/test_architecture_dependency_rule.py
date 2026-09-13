"""Architecture guard — the Dependency Rule, enforced instead of documented.

The DKS kernel is the single reasoning authority and the runtime is one of its
adapters: **the runtime depends on the port, and ``dks`` never imports the
runtime.** Every module under ``src/tessellum/dks/`` therefore has to stay pure
— it reads and *proposes* through Protocol ports, and storage lives in
``runtime/``.

Until now that was a convention held up by review. It is the invariant the whole
query-time-protocol integration rests on, and a convention is exactly the wrong
mechanism for an invariant: the violating import is one line, it works, its tests
pass, and the kernel has quietly become a runtime plugin. So this module reads
the import graph instead of trusting it.

What is checked, and why each form is checked rather than only the obvious one:

1. **Every import form**, by AST — ``import tessellum.runtime``,
   ``from tessellum.runtime import ...``, ``from tessellum.runtime.store import
   ...`` and the relative spellings (``from ..runtime import ...``). A guard that
   only knew one spelling would be a guard against typing, not against coupling.
2. **Imports nested anywhere** — inside a function, a method, a ``try``, or an
   ``if TYPE_CHECKING`` block. A deferred import is still a dependency: it
   couples the two packages' lifecycles and it is the form a violation actually
   takes, because a module-level one usually announces itself as a cycle.
3. **Dynamic imports**, by scanning for the dotted name in a string literal, so
   ``importlib.import_module("tessellum.runtime.store")`` cannot route around
   the AST check.
4. **The direction of the arrow** — ``runtime`` importing ``dks`` is asserted to
   be *present*, because the rule is about direction, not about distance. A test
   that only forbade one edge would still pass if the seam were deleted.

The complementary half — the kernel never *writes* — is asserted per phase in
the module smoke tests (each new ``dks`` module asserts its own source contains
no write statement); this file owns the import graph.

It also owns the storage side's matching invariant: **one table, one
definition**. The Tier-A ``relations`` cache is applied to two databases (the
runtime store and the registry sidecar) and used by three modules, and it briefly
existed as two divergent copies — different NOT NULLs, one extra column on one
side, and a ``PRAGMA table_info`` probe written to discover which shape the code
had been handed. Two definitions of one table is a coincidence rather than a
schema, so the shape is asserted identical across both appliers here.
"""

from __future__ import annotations

import ast
import re
import sqlite3
from pathlib import Path

import pytest

from tessellum.runtime.query_cache import QUERY_CACHE_SCHEMA
from tessellum.runtime.registry_store import RegistryStore
from tessellum.runtime.schema import SchemaSectionError, schema_section
from tessellum.runtime.store import RuntimeStore

SRC = Path(__file__).resolve().parents[2] / "src" / "tessellum"
DKS_ROOT = SRC / "dks"
RUNTIME_ROOT = SRC / "runtime"

FORBIDDEN_ROOT = "tessellum.runtime"
"""The one package ``dks`` may not depend on, in any spelling."""


def _dks_modules() -> list[Path]:
    """Every module under ``dks/``, subpackages included."""
    return sorted(DKS_ROOT.rglob("*.py"))


def _imported_modules(tree: ast.AST, *, package_parts: tuple[str, ...]) -> set[str]:
    """Every module name imported anywhere in ``tree``, absolutised.

    ``ast.walk`` rather than a scan of ``tree.body``: an import inside a
    function, a ``try``, or an ``if TYPE_CHECKING`` block is still an import, and
    the deferred forms are the ones a violation reaches for. Relative imports are
    resolved against ``package_parts`` so ``from ..runtime import store`` is
    reported as ``tessellum.runtime.store``.
    """
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                base = node.module or ""
            else:
                # level=1 is the module's own package, level=2 its parent, ...
                anchor = package_parts[: len(package_parts) - (node.level - 1)]
                base = ".".join((*anchor, node.module) if node.module else anchor)
            imported.add(base)
            for alias in node.names:
                imported.add(f"{base}.{alias.name}" if base else alias.name)
    return imported


def _package_parts(path: Path) -> tuple[str, ...]:
    """The dotted package the module at ``path`` lives in.

    ``dks/core.py`` and ``dks/__init__.py`` both answer ``tessellum.dks``, which
    is what a relative import's ``level=1`` resolves against.
    """
    parts = path.relative_to(SRC.parent).with_suffix("").parts
    return parts[:-1]


def _violates(name: str) -> bool:
    """Whether an imported name reaches into the forbidden package."""
    return name == FORBIDDEN_ROOT or name.startswith(f"{FORBIDDEN_ROOT}.")


# ── the rule itself ─────────────────────────────────────────────────────────


def test_the_dks_package_is_populated() -> None:
    """A guard over an empty file list is a guard over nothing."""
    modules = _dks_modules()
    assert len(modules) > 20
    names = {path.name for path in modules}
    # The query-time-protocol modules, named so a silent rename cannot drop one
    # of them out of the checked set.
    assert {
        "claim_identity.py",
        "consolidation.py",
        "demotion.py",
        "entity_registry.py",
        "memory_port.py",
        "memory_tiers.py",
        "query_protocol.py",
        "reach.py",
        "resolve_entity.py",
        "status.py",
    } <= names


@pytest.mark.parametrize("module", _dks_modules(), ids=lambda p: p.name)
def test_no_dks_module_imports_the_runtime(module: Path) -> None:
    """No module under ``dks/`` imports ``tessellum.runtime``, in any spelling.

    If this fails, the fix is never to relax the assertion: move the persistence
    behind a Protocol port declared in ``dks/`` and put the backing
    implementation in ``runtime/``, which is how every storage-touching phase of
    the query-time protocol is wired (``RegistrySource``/``RegistrySink``,
    ``QueryCacheSource``/``FeedbackSink``, ``LogAppendPort``).
    """
    source = module.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(module))
    offenders = sorted(
        name
        for name in _imported_modules(tree, package_parts=_package_parts(module))
        if _violates(name)
    )
    assert not offenders, (
        f"{module.relative_to(SRC.parent)} imports {offenders} — the Dependency Rule "
        "says the runtime depends on the kernel's port, never the other way. Declare a "
        "Protocol port in dks/ and back it from runtime/."
    )


@pytest.mark.parametrize("module", _dks_modules(), ids=lambda p: p.name)
def test_no_dks_module_names_the_runtime_dynamically(module: Path) -> None:
    """``importlib.import_module("tessellum.runtime...")`` is the same violation.

    A dotted string is invisible to the AST import check, so the literal is
    forbidden too. Docstrings and comments are exempt — describing the boundary
    is the opposite of crossing it — which is why only string *constants* in
    executable position are scanned.
    """
    tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
    docstrings = {
        ast.get_docstring(node, clean=False)
        for node in ast.walk(tree)
        if isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        )
    }
    offenders = sorted(
        {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value not in docstrings
            and FORBIDDEN_ROOT in node.value
        }
    )
    assert not offenders, (
        f"{module.relative_to(SRC.parent)} names the runtime in a string literal: "
        f"{offenders}. A dynamic import is a dependency the import graph cannot see."
    )


@pytest.mark.parametrize(
    "source",
    [
        "import tessellum.runtime",
        "import tessellum.runtime.store as store",
        "from tessellum.runtime import store",
        "from tessellum.runtime.store import RuntimeStore",
        "from ..runtime import store",
        "from ..runtime.store import RuntimeStore",
        "def f():\n    from tessellum.runtime.store import RuntimeStore\n",
        "try:\n    import tessellum.runtime\nexcept ImportError:\n    pass\n",
        (
            "from typing import TYPE_CHECKING\n"
            "if TYPE_CHECKING:\n"
            "    from tessellum.runtime.store import RuntimeStore\n"
        ),
    ],
)
def test_the_detector_fires_on_every_spelling(source: str) -> None:
    """The guard is only worth its runtime if it would actually catch a violation.

    Nine spellings of the same coupling, including the three deferred forms a real
    violation takes (function-local, guarded by ``try``, and ``TYPE_CHECKING``).
    Without this the suite could go green because the detector sees nothing rather
    than because there is nothing to see.
    """
    tree = ast.parse(source)
    reached = _imported_modules(tree, package_parts=("tessellum", "dks"))
    assert any(_violates(name) for name in reached), reached


def test_the_detector_passes_a_permitted_neighbour() -> None:
    """And it does not fire on the imports the kernel is *supposed* to make.

    ``dks`` depending on ``composer``, ``bb`` and its own submodules is the
    designed shape; a guard that flagged those would be read as noise and then
    ignored.
    """
    source = (
        "from tessellum.bb.types import BBType\n"
        "from tessellum.composer.signoff import SignOffPolicy\n"
        "from tessellum.dks.capability import CapabilityEffect\n"
        "from .status import compute_statuses\n"
    )
    reached = _imported_modules(ast.parse(source), package_parts=("tessellum", "dks"))
    assert not [name for name in reached if _violates(name)]


def test_the_arrow_points_the_other_way() -> None:
    """``runtime`` DOES import ``dks`` — the rule is direction, not distance.

    Without this clause the guard above is satisfiable by severing the seam
    entirely, which would be a different architecture rather than a compliant
    one. The storage modules the query-time protocol added are the concrete
    adapters, so each is expected here by name.
    """
    importers: dict[str, set[str]] = {}
    for module in sorted(RUNTIME_ROOT.rglob("*.py")):
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        reached = {
            name
            for name in _imported_modules(tree, package_parts=_package_parts(module))
            if name == "tessellum.dks" or name.startswith("tessellum.dks.")
        }
        if reached:
            importers[module.name] = reached
    assert importers, "runtime imports nothing from dks — the port seam is gone"
    assert {"registry_store.py", "query_cache.py"} <= set(importers)


PROTOCOL_MODULES = (
    "claim_identity.py",
    "consolidation.py",
    "demotion.py",
    "entity_registry.py",
    "memory_port.py",
    "memory_tiers.py",
    "query_protocol.py",
    "reach.py",
    "resolve_entity.py",
    "status.py",
)
"""The query-time-protocol modules, each declared **pure** by its own phase."""


@pytest.mark.parametrize("name", PROTOCOL_MODULES)
def test_the_protocol_modules_hold_no_storage_primitive(name: str) -> None:
    """The pure modules reach for neither a database handle nor a filesystem path.

    The import-graph rule above is the structural half of "the kernel never
    writes"; this is the direct half, and it is scoped to the modules whose
    phases declared purity rather than to the whole package (``retrieval_client``
    legitimately types a read-only ``db_path``, and ``persistence`` /
    ``meta.runtime`` are the older warrant/event-JSON design this rule exists to
    stop spreading). Persistence for these ten is a runtime concern reached
    through a Protocol port — ``RegistrySource``/``RegistrySink``,
    ``QueryCacheSource``/``FeedbackSink``, ``LogAppendPort``.
    """
    module = DKS_ROOT / name
    tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
    reached = sorted(
        primitive
        for primitive in _imported_modules(tree, package_parts=_package_parts(module))
        if primitive in {"sqlite3", "pathlib"} or primitive.startswith("pathlib.")
    )
    assert not reached, (
        f"dks/{name} imports {reached} — a pure module that can open a store will "
        "eventually own one. Declare a port instead."
    )


# ── the storage side: one table, one definition ─────────────────────────────


def _relations_shape(path: Path) -> list[tuple[str, str, int]]:
    """``(name, declared type, notnull)`` per column of ``relations``."""
    conn = sqlite3.connect(path)
    try:
        return [(row[1], row[2], row[3]) for row in conn.execute("PRAGMA table_info(relations)")]
    finally:
        conn.close()


def test_the_tier_a_table_has_one_definition_and_two_appliers(tmp_path: Path) -> None:
    """The runtime database and the registry sidecar agree on ``relations``.

    Both apply the ``tier_a_relations`` section of ``schema.sql`` — the runtime
    store as part of the whole file, the sidecar through
    :func:`~tessellum.runtime.schema.schema_section` — so the shapes are equal by
    construction rather than by care. Asserted anyway: the failure this replaces
    was a *silent* divergence in which each side worked alone and a row written
    through one door violated the other's constraints.
    """
    runtime_store = RuntimeStore.open(tmp_path / "runtime.db")
    registry = RegistryStore.open(tmp_path / "registry.db")
    shape = _relations_shape(runtime_store.path)
    assert shape == _relations_shape(registry.path)
    # The columns that make a cached relation citable and layerable are required,
    # not hopeful — a row missing any of them is unusable rather than merely thin.
    required = {name for name, _type, notnull in shape if notnull}
    assert {
        "subject_id",
        "predicate",
        "object_ref",
        "object_kind",
        "evidence_note",
        "evidence_locator",
        "origin",
    } <= required
    # ... and the validity interval is deliberately NULLABLE: an undated authored
    # fact is legitimate, while a role answer without an interval is not — which
    # is a read-time concern, not a column constraint.
    assert {"valid_from", "valid_to"}.isdisjoint(required)


def test_the_tier_b_section_defines_only_its_own_two_tables() -> None:
    """The Tier-B store applies a section, not the whole schema.

    A store that may be opened on a sidecar database has no business creating a
    job queue there, and it does not define the Tier-A table it writes into. Both
    facts are properties of the slice, so they are checked on the slice.
    """
    section = schema_section("tier_b_query_cache")
    created = set(re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)", section))
    assert created == {"query_cache", "feedback"}
    assert QUERY_CACHE_SCHEMA.endswith(section)


def test_a_renamed_schema_section_is_an_error_not_an_empty_string() -> None:
    """An unknown section refuses rather than returning DDL that creates nothing.

    An empty string would apply cleanly and fail much later, from inside a
    transaction, as a missing-table error three frames from the rename.
    """
    with pytest.raises(SchemaSectionError):
        schema_section("no_such_section")
