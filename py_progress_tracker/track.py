import colorama
import cpuinfo
import inspect
import json
import os
import pathlib
import platform
import psutil
import tabulate
import termcolor
import traceback
import urllib

from .state import MEASUREMENTS, METRICS, ALERTS

def track(targets):
    colorama.init()

    samples = os.environ.get("PROGRESS_SAMPLES", "30")
    output_path = os.environ.get("PROGRESS_OUTPUT", "progress.json")
    output_indent = os.environ.get("PROGRESS_OUTPUT_INDENT", None)

    samples = int(samples)
    output_path = pathlib.Path(output_path)
    if output_indent is not None:
        output_indent = int(output_indent)

    machine_specs = []

    machine_cpu = cpuinfo.get_cpu_info()["brand_raw"].replace("(R)", "®").replace("(TM)", "™")
    machine_specs.append(["CPU", machine_cpu])

    machine_vcpu = os.environ.get("PROGRESS_MACHINE_VCPU", None)
    if machine_vcpu is not None:
        machine_specs.append(["vCPU", machine_vcpu])

    machine_ram = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"
    machine_specs.append(["RAM", machine_ram])

    machine_os = os.environ.get("PROGRESS_MACHINE_OS", None)
    if machine_os is None:
        machine_os = f"{platform.system()} {platform.release()}"
    machine_specs.append(["OS", machine_os])

    machine_name = os.environ.get("PROGRESS_MACHINE_NAME", None)
    if machine_name is None:
        machine_name = platform.node()
    machine_name = machine_name.strip()

    machine_id = machine_name.lower()
    machine_id = machine_id.replace(" ", "-")
    machine_id = machine_id.replace("_", "-")
    machine_id = machine_id.replace(".", "-")
    machine_id = machine_id.replace("(", "")
    machine_id = machine_id.replace(")", "")
    machine_id = machine_id.replace("$/h", "-dollars-per-hour")
    machine_id = machine_id.strip()
    machine_id = urllib.parse.quote_plus(machine_id)

    machine = {"id": machine_id, "name": machine_name, "specs": machine_specs}

    def inner(main):
        output = None
        if output_path.exists():
            with open(output_path, "r") as output_file:
                try:
                    output = json.load(output_file)
                except:
                    pass

        if output is None:
            output = {"machine": {}, "metrics": {}, "targets": {}}

        output["machine"] = machine

        with open(output_path, "w") as output_file:
            json.dump(output, output_file, indent=output_indent, ensure_ascii=False)

        source = inspect.getsource(inspect.getmodule(main))
        for target in targets:
            MEASUREMENTS.clear()
            METRICS.clear()

            id = target["id"]
            name = target["name"]
            parameters = target.get("parameters", {})

            if id in output["targets"]:
                target = output["targets"][id]
            else:
                target = {}

            target["name"] = name
            target["code"] = source

            for i in range(1, samples + 1):
                ALERTS.clear()

                title = f"Sample #{i} of {name}"

                print()
                print(termcolor.colored(f"{title}", "yellow"))

                print(termcolor.colored(f"{'-' * len(title)}", "cyan"))
                try:
                    main(**parameters)
                except:
                    print(traceback.format_exc(), end="")
                    target["working"] = False
                    if "measurements" in target:
                        del target["measurements"]
                    break
                finally:
                    print(termcolor.colored(f"{'-' * len(title)}", "cyan"))
            else:
                target["working"] = True
                target["measurements"] = {}
                target["alerts"] = list(ALERTS)

                for metric, label in METRICS.items():
                    output["metrics"][metric] = {"label": label}

                title = f"{name} over {samples} samples"

                print()
                print(termcolor.colored(f"{title}", "green"))

                print(termcolor.colored(f"{'-' * len(title)}", "cyan"))
                table = []
                for metric, value in MEASUREMENTS.items():
                    if len(value) > 0:
                        average = sum(value) / len(value)
                        target["measurements"][metric] = average
                        table.append([output["metrics"][metric]["label"], average])
                print(tabulate.tabulate(table, tablefmt="grid", numalign="right", floatfmt=".6f"))
                print(termcolor.colored(f"{'-' * len(title)}", "cyan"))

            if not target["working"]:
                title = f"{name} over {samples} samples"

                print()
                print(termcolor.colored(f"{title}", "red"))

                print(termcolor.colored(f"{'-' * len(title)}", "cyan"))
                print("Not Working")
                print(termcolor.colored(f"{'-' * len(title)}", "cyan"))

            output["targets"][id] = target
            with open(output_path, "w") as output_file:
                json.dump(output, output_file, indent=output_indent, ensure_ascii=False)

        print()

    return inner
