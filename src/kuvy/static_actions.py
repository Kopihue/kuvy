from kopilogs.paint import paint

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

def help():
    paint(
        paint("Usage: kuvy"),
        paint("[flag]").bold().blue(),
        paint("[action]").bold().green(),
        paint("[arg]").bold().magenta(),
    ).show()
    paint("").show()
    paint(
        paint("[action]").bold().green(),
        paint("[arg]").bold().magenta(),
    ).show()
    print("-" * 25)
    paint(
        paint("[help]").bold().green(),
        paint("[no arg]:").bold().magenta(),
        paint("Shows help panel").bold(),
    ).show()
    paint(
        paint("[new]").bold().green(),
        paint(" [name]: ").bold().magenta(),
        paint(" Creates new project \"name\"").bold(),
    ).show()
    paint(
        paint("[run]").bold().green(),
        paint(" [file]: ").bold().magenta(),
        paint(" Executes \"file\", which has to be specified in pyproject.toml").bold(),
    ).show()
    paint("").show()
    paint("Flags:").show()
