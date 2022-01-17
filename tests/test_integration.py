import json
import os
import subprocess


def test_system():
    if os.path.exists("progress.json"):
        os.remove("progress.json")

    os.environ["PROGRESS_SAMPLES"] = "3"

    os.environ["PROGRESS_MACHINE_VCPU"] = "4"
    os.environ["PROGRESS_MACHINE_OS"] = "Ubuntu"
    os.environ["PROGRESS_MACHINE_NAME"] = "Workstation"

    subprocess.run(["python", "examples/pi-estimation.py"], capture_output=True)
    with open("examples/pi-estimation.py") as file:
        code = file.read()

    assert os.path.exists("progress.json")
    with open("progress.json") as file:
        progress = json.load(file)

        def check_machine(machine):
            assert "id" in machine
            assert machine["id"] == "workstation"

            assert "name" in machine
            assert machine["name"] == "Workstation"

            assert "specs" in machine
            specs = machine["specs"]

            assert isinstance(specs, list)
            assert len(specs) == 4

            assert ["vCPU", "4"] in specs
            assert ["OS", "Ubuntu"] in specs

        def check_metrics(metrics):
            assert "time-ms" in metrics
            time_ms = metrics["time-ms"]

            assert "label" in time_ms
            assert time_ms["label"] == "Time (ms)"

            assert "estimation" in metrics
            estimation = metrics["estimation"]

            assert "label" in estimation
            assert estimation["label"] == "Estimation"

            assert "error-percent" in metrics
            error_percent = metrics["error-percent"]

            assert "label" in error_percent
            assert error_percent["label"] == "Error (%)"

        def check_targets(targets):
            for samples in [1000, 10000, 100000, 1000000]:
                id = f"monte-carlo-pi-{samples}-samples"

                assert id in targets
                target = targets[id]

                assert "name" in target
                assert target["name"] == f"Estimating π with Monte Carlo ({samples} samples)"

                assert "code" in target
                assert target["code"] == code

                assert "working" in target
                assert target["working"]

        assert "machine" in progress
        check_machine(progress["machine"])

        assert "metrics" in progress
        check_metrics(progress["metrics"])

        assert "targets" in progress
        check_targets(progress["targets"])
