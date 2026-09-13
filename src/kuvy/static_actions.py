from pathlib import Path
from textwrap import dedent
from venv import EnvBuilder

def create_project(name: str):
    main_py = dedent(
        f"""\
        import sys

        def main() -> int:
            print("Hola, mundo!")

            return 0

        if __name__ == "__main__":
            sys.exit(main())
        """
    )

    pyproject_toml = dedent(
        f"""\
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [project]
        name = "{name}"
        version = "0.1.0"
        dependencies = [
        ]

        [project.scripts]
        {name} = "{name}.main:main"

        [tool.kuvy.run-paths]
        main = "src/{name}/main.py"
        tests = "tests/tests.py"
        """
    )

    written_files = {
        "main.py": main_py,
        "pyproject.toml": pyproject_toml,
    }

    project = Path().cwd().joinpath(name)

    if project.exists():
        raise FileExistsError(f"\"{name}\" already exists under: {project.resolve()}")

    project.mkdir()

    dirs = [
        project.joinpath("src", name),
        project.joinpath("tests"),
    ]

    files = [
        project.joinpath("src", name, "main.py"),
        project.joinpath("tests", "tests.py"),
        project.joinpath("pyproject.toml"),
    ]

    for dir in dirs:
        dir.mkdir(parents=True)

    for file in files:
        file.touch()

        if file.name in ("main.py", "pyproject.toml"):
            with open(file, "w") as f:
                f.write(written_files[file.name])

    EnvBuilder().create(project.joinpath(".venv"))
