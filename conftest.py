import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--real-db",
        action="store_true",
        default=False,
        help="Ejecutar los tests utilizando la base de datos real.",
    )


def _remove_django_db_markers(node):
    """
    Elimina django_db del nodo y de todos sus padres.

    Esto es necesario porque pytestmark puede estar definido
    a nivel de módulo o clase y ser heredado por el test.
    """
    while node is not None:
        node.own_markers = [
            marker
            for marker in node.own_markers
            if marker.name != "django_db"
        ]
        node = node.parent


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--real-db"):
        return

    for item in items:
        _remove_django_db_markers(item)


@pytest.fixture(autouse=True)
def allow_real_db(request, django_db_blocker):
    """
    En modo --real-db permite que los tests accedan directamente
    a la base de datos configurada en Django.
    """
    if request.config.getoption("--real-db"):
        with django_db_blocker.unblock():
            yield
    else:
        yield