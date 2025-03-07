import sys
from pathlib import Path
from importlib.util import find_spec
from typing_extensions import Protocol, runtime_checkable

PRISMA_INIT_CONTENTS = "__title__ = 'prisma'"


@runtime_checkable
class SourceLoader(Protocol):
    def get_filename(self) -> str: ...


def main(*args: str) -> None:
    if args:
        pkg_name = args[0]
    else:
        pkg_name = 'prisma'

    cleanup(pkg_name=pkg_name)


def cleanup(pkg_name: str = 'prisma') -> None:
    """Remove python files that are auto-generated by Prisma Client Python"""

    spec = find_spec(pkg_name)
    if spec is None:
        raise RuntimeError(f'Could not resolve package: {pkg_name}')

    loader = spec.loader
    if loader is None:
        raise RuntimeError(f'No loader defined for: {pkg_name}')

    if not isinstance(loader, SourceLoader):
        raise RuntimeError(f'Received unresolvable import loader: {loader}')

    # ensure the package we've been given is actually a Prisma Client Python package
    # we don't want to make it easy for users to accidentaly delete files from
    # a non Prisma Client Python package
    pkg_path = Path(loader.get_filename())
    if PRISMA_INIT_CONTENTS not in pkg_path.read_text():
        raise RuntimeError('The given package does not appear to be a Prisma Client Python package.')

    # as we rely on prisma to cleanup the templates for us
    # we have to make sure that prisma is importable and
    # if any template rendered incorrect syntax or any other
    # kind of error that wasn't automatically cleaned up,
    # prisma will raise an error when imported,
    # removing prisma/client.py fixes this as it is
    # the only default entrypoint to generated code.
    file = pkg_path.parent / 'client.py'
    if file.exists():
        file.unlink()

    # the `prisma` package will always exist even when using a custom output
    # location so it is safe to use here
    from prisma.generator.generator import cleanup_templates

    cleanup_templates(rootdir=pkg_path.parent)
    print(f'Successfully removed all auto-generated files from {pkg_path}')  # noqa: T201


if __name__ == '__main__':
    main(*sys.argv[1:])
