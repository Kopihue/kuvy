from pathlib import Path
import subprocess
import tomllib
import tomli_w

class Kuvy:
    def __init__(self):
        current = [Path().cwd(), *Path().cwd().parents]

        self.project = None
        for path in current:
            venv = path.joinpath(".venv")

            if venv.exists():
                self.project = venv.parent
                break

        if self.project is None:
            raise RuntimeError("Not in a project!")

        self.python = self.project.joinpath(".venv", "bin", "python")
        self.pyproject = self.project.joinpath("pyproject.toml")

    def run(self, file: str):
        data = self._pyproject_read_kuvy()["run-paths"]

        if file not in data:
            raise ValueError(f"Unable to run \"{file}\" as it's not specified in pyproject.toml")

        subprocess.run([self.python, self.project.joinpath(data[file])])

    def _pyproject_read(self) -> dict:
        with open(self.pyproject, "rb") as f:
            return tomllib.load(f)

    def _pyproject_read_kuvy(self) -> dict:
        try:
            self._pyproject_read()["tool"]
        except KeyError:
            self._pyproject_write_kuvy()

        return self._pyproject_read()["tool"]["kuvy"]

    def _pyproject_write(self, data: dict):
        with open(self.pyproject, "wb") as f:
            tomli_w.dump(data, f)

    def _pyproject_write_kuvy(self):
        data = self._pyproject_read()
        data.update({
            "tool": {
                "kuvy": {
                    "run-paths": {
                        "main": "src/kuvy/main.py", "tests": "tests/tests.py",
                    }
                }
            }
        })
        self._pyproject_write(data)
