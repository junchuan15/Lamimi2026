import os
from pathlib import Path
import papermill as pm

def get_project_root(markers=("requirements.txt", "README.md")):
    path = Path(__file__).resolve()
    for parent in path.parents:
        if any((parent / marker).exists() for marker in markers):
            return parent
    return path.parents[2]


def run_notebook(input_notebook: Path, output_notebook: Path = None, parameters: dict = None, overwrite: bool = False):
    if parameters is None:
        parameters = {}
    input_path = Path(input_notebook)
    if output_notebook is None:
        if overwrite:
            output_path = input_path
        else:
            output_path = input_path.with_name(input_path.stem + "_executed.ipynb")
    else:
        output_path = Path(output_notebook)
        if overwrite:
            output_path = input_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pm.execute_notebook(
        input_path=str(input_path),
        output_path=str(output_path),
        parameters=parameters,
    )
    return output_path

def get_notebook_path(stage: str, notebook_name: str, subset: str = None):
    root = get_project_root()
    base = root / "src" / stage
    if stage == "powerbi" and subset:
        base /= subset
    return base / notebook_name