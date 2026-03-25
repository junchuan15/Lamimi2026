from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import sys
sys.path.append('../..')
from utils.notebook_runner import run_notebook


def run_notebook_task(notebook_path: str):
    p = Path(notebook_path)
    if not p.exists():
        raise FileNotFoundError(f"Notebook not found: {p}")
    run_notebook(p, overwrite=True)


def notebook_tasks_for_stage(dag, stage_id, folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        return []

    tasks = []
    for nb in sorted(folder.glob("*.ipynb")):
        task_id = f"{stage_id}_{nb.stem}".replace("-", "_").replace(" ", "_")
        task = PythonOperator(
            task_id=task_id,
            python_callable=run_notebook_task,
            op_kwargs={"notebook_path": str(nb)},
            dag=dag,
        )
        tasks.append(task)

    for prev, next in zip(tasks, tasks[1:]):
        prev >> next

    return tasks


with DAG(
    dag_id="notebook_pipeline_all_stages",
    default_args={
        "owner": "airflow",
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    description="Run all notebooks in sequence: landing -> staging -> ml -> powerbi/Dimension -> powerbi/Fact",
    start_date=datetime(2026, 3, 25),
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["notebook_orchestrator"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    project_root = Path(__file__).resolve().parents[2]
    stage_definitions = [
        ("landing", project_root / "src" / "landing"),
        ("staging", project_root / "src" / "staging"),
        ("ml", project_root / "src" / "ml"),
        ("powerbi_dimension", project_root / "src" / "powerbi" / "Dimension"),
        ("powerbi_fact", project_root / "src" / "powerbi" / "Fact"),
    ]

    # Build task chains for each stage and link stages together
    previous_stage_last_task = start
    for stage_id, stage_dir in stage_definitions:
        stage_tasks = notebook_tasks_for_stage(dag, stage_id, stage_dir)
        if not stage_tasks:
            continue
        previous_stage_last_task >> stage_tasks[0]
        previous_stage_last_task = stage_tasks[-1]

    previous_stage_last_task >> end
