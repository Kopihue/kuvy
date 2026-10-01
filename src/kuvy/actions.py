from pathlib import Path
from textwrap import dedent
import venv
import tomllib
import tomli_w
import subprocess

class ActionsUtils:
    def __init__(self):
        current = Path().cwd()
        
        venv = None
        for dir in [current, *current.parents]:
            dir = dir.joinpath(".venv")

            if dir.exists():
                venv = dir
                break

        if not venv:
            raise FileNotFoundError("Not in a Python virtual environment!")

        self.venv = venv
        self.project = self.venv.parent
        self.project_name = self.project.name
        self.pyproject = self.project.joinpath("pyproject.toml")
        self.python = self.venv.joinpath("bin", "python3")

        with open(self.pyproject, "rb") as f:
            self.pyproject_data = tomllib.load(f)

    def get_kuvy_field(self) -> dict:
        try:
            return self.pyproject_data["tool"]["kuvy"]
        except KeyError:
            self.generate_kuvy_field()
            return self.pyproject_data["tool"]["kuvy"]

    def generate_kuvy_field(self):
        field = {
            "tool": {
                "kuvy": {
                    "run": {
                        "main": f"src/{self.project_name}/main.py",
                        "tests": "tests/tests.py"
                    }
                }
            }
        }

        self.pyproject_data.update(field)
        with open(self.pyproject, "wb") as f:
            tomli_w.dump(self.pyproject_data, f)

    def generate_content_kuvy_field(self, content: dict):
        kuvy = self.pyproject_data
        kuvy.update(content)

        with open(self.pyproject, "wb") as f:
            tomli_w.dump(kuvy, f)

class Actions(ActionsUtils):
    def __init__(self):
        super().__init__()

    def run(self, file: str, args: list[str] = []):
        try:
            run = self.get_kuvy_field()["run"]
        except KeyError:
            self.generate_content_kuvy_field({
                "tool": {
                    "kuvy": {
                        "run": {
                            "main": f"src/{self.project_name}/main.py",
                            "tests": "tests/tests.py"
                        }
                    }
                }
            })
            run = self.get_kuvy_field()["run"]

        try:
            file = run[file]
        except KeyError:
            raise ValueError(f"{file} to execute is not in tool.kuvy.run!")

        subprocess.run([self.python, file, *args])

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

        [tool.kuvy.run]
        main = "src/{name}/main.py"
        tests = "tests/tests.py"
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
