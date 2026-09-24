from pathlib import Path
from textwrap import dedent
import venv

def new(name: str):
    MAIN = dedent(
        f"""\
        import sys

        def main() -> int:
            print("hola, mundo.")

            return 0;

        if __name__ == "__main__":
            sys.exit(main())
        """
    )

    PYPROJECT = dedent(
        f"""\
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [project]
        name = "{name}"
        version = "0.1.0"
        description = ""
        readme = "README.md"
        requires-python = ""
        dependencies = [

        ]

        [project.scripts]
        {name} = "{name}:main.main"
        """
    )

    README = dedent(
        f"""\
        # {name}
        """
    )

    project = Path.cwd().joinpath(name)
    
    if project.exists():
        raise FileExistsError(f"Project already exists at: {project}")

    dirs = [
        project.joinpath("src", name),
        project.joinpath("tests"),
    ]

    files = [
        project.joinpath("src", name, "main.py"),
        project.joinpath("src", name, "__init__.py"),
        project.joinpath("pyproject.toml"),
        project.joinpath("tests", "tests.py"),
        project.joinpath("README.md"),
        project.joinpath(".gitignore"),
    ]

    for dir in dirs:
        dir.mkdir(parents=True)

    for file in files:
        file.touch()

        if file.name == "pyproject.toml":
            with open(file, "w") as f:
                f.write(PYPROJECT)

        if file.name == "main.py":
            with open(file, "w") as f:
                f.write(MAIN)

        if file.name == "README.md":
            with open(file, "w") as f:
                f.write(README)

    virtualenv = venv.EnvBuilder()
    virtualenv.create(project.joinpath(".venv"))

def help():
    print("Usage: kuvy [action] [args]")
