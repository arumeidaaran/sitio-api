from packaging.version import Version

from __version__ import __version__


def test_version_de_la_aplicacion_debe_cumplir_pep_440():
    version = Version(__version__)

    assert str(version) == __version__, (
        'La versión debe utilizar la forma canónica de PEP 440.'
    )
    assert len(version.release) == 3, (
        'La versión debe contener major.minor.patch.'
    )
    assert version.epoch == 0, (
        'La versión utilizada como etiqueta OCI no admite epoch.'
    )
    assert version.local is None, (
        'La versión utilizada como etiqueta OCI no admite versión local.'
    )
