"""The module's envelope: what must hold before any behaviour exists.

Not a placeholder. Each of these breaks for a real reason — a package that stopped being
importable, a manifest that stopped declaring what CI reads.
"""

from pathlib import Path

import loans

MANIFEST = Path(__file__).resolve().parents[1] / "MANIFEST.yaml"


def test_the_package_is_importable_from_the_declared_source_root() -> None:
    assert loans.__doc__, "the package must carry its own description"


def test_the_manifest_is_where_the_fitness_functions_expect_it() -> None:
    assert MANIFEST.is_file(), f"{MANIFEST} missing: the fitness functions read it"
