# Progress

## Installation

### With pip

```
pip install py-progress-tracker
```

### With poetry

```
poetry add py-progress-tracker
```

## Usage

Here is an example benchmark that estimates π using monte carlo.

```python
import math
import py_progress_tracker as progress
import random

def estimate_pi(samples):
    circle_points = 0
    square_points = 0

    for i in range(samples):
        rand_x = random.uniform(-1, 1)
        rand_y = random.uniform(-1, 1)

        origin_dist = rand_x**2 + rand_y**2
        if origin_dist <= 1:
            circle_points += 1

        square_points += 1

    return 4 * circle_points / square_points

@progress.track([
    {
        "id": "monte-carlo-pi-1000-samples",
        "name": "Estimating π with Monte Carlo (1000 samples)",
        "parameters": {
            "samples": 1000,
        },
    },
    {
        "id": "monte-carlo-pi-10000-samples",
        "name": "Estimating π with Monte Carlo (10000 samples)",
        "parameters": {
            "samples": 10000,
        },
    },
    {
        "id": "monte-carlo-pi-100000-samples",
        "name": "Estimating π with Monte Carlo (100000 samples)",
        "parameters": {
            "samples": 100000,
        },
    },
    {
        "id": "monte-carlo-pi-1000000-samples",
        "name": "Estimating π with Monte Carlo (1000000 samples)",
        "parameters": {
            "samples": 1000000,
        },
    },
])
def main(samples):
    with progress.measure(id="time-ms", label="Time (ms)", alert=(">", samples * 0.001)):
        estimation = estimate_pi(samples)

    print(f"Estimation: {estimation:.6f}")
    progress.measure(id="estimation", label="Estimation", value=estimation)

    error = abs(estimation - math.pi)
    error_percent = (error / math.pi) * 100
    acceptable_error_percent = 5

    print(f"Error: {error_percent:.2f}%")
    progress.measure(
        id="error-percent",
        label="Error (%)",
        value=error_percent,
        alert=(">", acceptable_error_percent),
    )
```

When you run this script directly like `python examples/pi-estimation.py`, this is the output you get.

```
Sample #1 of Estimating π with Monte Carlo (1000 samples)
---------------------------------------------------------
Estimation: 3.100000
Error: 1.32%
---------------------------------------------------------

Sample #2 of Estimating π with Monte Carlo (1000 samples)
---------------------------------------------------------
Estimation: 3.148000
Error: 0.20%
---------------------------------------------------------

...

Sample #29 of Estimating π with Monte Carlo (1000 samples)
----------------------------------------------------------
Estimation: 3.116000
Error: 0.81%
----------------------------------------------------------

Sample #30 of Estimating π with Monte Carlo (1000 samples)
----------------------------------------------------------
Estimation: 3.080000
Error: 1.96%
----------------------------------------------------------

Estimating π with Monte Carlo (1000 samples) over 30 samples
------------------------------------------------------------
+------------+----------+
| Time (ms)  | 0.616535 |
+------------+----------+
| Estimation | 3.132400 |
+------------+----------+
| Error (%)  | 1.258778 |
+------------+----------+
------------------------------------------------------------

Sample #1 of Estimating π with Monte Carlo (10000 samples)
----------------------------------------------------------
Estimation: 3.120000
Error: 0.69%
----------------------------------------------------------

Sample #2 of Estimating π with Monte Carlo (10000 samples)
----------------------------------------------------------
Estimation: 3.147200
Error: 0.18%
----------------------------------------------------------

...

Sample #29 of Estimating π with Monte Carlo (10000 samples)
-----------------------------------------------------------
Estimation: 3.136800
Error: 0.15%
-----------------------------------------------------------

Sample #30 of Estimating π with Monte Carlo (10000 samples)
-----------------------------------------------------------
Estimation: 3.134800
Error: 0.22%
-----------------------------------------------------------

Estimating π with Monte Carlo (10000 samples) over 30 samples
-------------------------------------------------------------
+------------+----------+
| Time (ms)  | 6.283108 |
+------------+----------+
| Estimation | 3.143840 |
+------------+----------+
| Error (%)  | 0.346368 |
+------------+----------+
-------------------------------------------------------------

Sample #1 of Estimating π with Monte Carlo (100000 samples)
-----------------------------------------------------------
Estimation: 3.141600
Error: 0.00%
-----------------------------------------------------------

Sample #2 of Estimating π with Monte Carlo (100000 samples)
-----------------------------------------------------------
Estimation: 3.141880
Error: 0.01%
-----------------------------------------------------------

...

Sample #29 of Estimating π with Monte Carlo (100000 samples)
------------------------------------------------------------
Estimation: 3.146240
Error: 0.15%
------------------------------------------------------------

Sample #30 of Estimating π with Monte Carlo (100000 samples)
------------------------------------------------------------
Estimation: 3.141040
Error: 0.02%
------------------------------------------------------------

Estimating π with Monte Carlo (100000 samples) over 30 samples
--------------------------------------------------------------
+------------+-----------+
| Time (ms)  | 59.226386 |
+------------+-----------+
| Estimation |  3.141260 |
+------------+-----------+
| Error (%)  |  0.161844 |
+------------+-----------+
--------------------------------------------------------------

Sample #1 of Estimating π with Monte Carlo (1000000 samples)
------------------------------------------------------------
Estimation: 3.145180
Error: 0.11%
------------------------------------------------------------

Sample #2 of Estimating π with Monte Carlo (1000000 samples)
------------------------------------------------------------
Estimation: 3.141740
Error: 0.00%
------------------------------------------------------------

...

Sample #29 of Estimating π with Monte Carlo (1000000 samples)
-------------------------------------------------------------
Estimation: 3.144168
Error: 0.08%
-------------------------------------------------------------

Sample #30 of Estimating π with Monte Carlo (1000000 samples)
-------------------------------------------------------------
Estimation: 3.142860
Error: 0.04%
-------------------------------------------------------------

Estimating π with Monte Carlo (1000000 samples) over 30 samples
---------------------------------------------------------------
+------------+------------+
| Time (ms)  | 585.633898 |
+------------+------------+
| Estimation |   3.142039 |
+------------+------------+
| Error (%)  |   0.045782 |
+------------+------------+
---------------------------------------------------------------
```

Furthermore, a json file called `progress.json` is created in your working diretory with the following content.

```json
{
  "machine": {
    "id": "workstation",
    "name": "Workstation",
    "specs": [
      [
        "CPU",
        "Intel® Core™ i7-1065G7 CPU @ 1.30GHz"
      ],
      [
        "RAM",
        "15.41 GB"
      ],
      [
        "OS",
        "Linux 5.12.13-arch1-2"
      ]
    ]
  },
  "metrics": {
    "time-ms": {
      "label": "Time (ms)"
    },
    "estimation": {
      "label": "Estimation"
    },
    "error-percent": {
      "label": "Error (%)"
    }
  },
  "targets": {
    "monte-carlo-pi-1000-samples": {
      "name": "Estimating π with Monte Carlo (1000 samples)",
      "code": "...",
      "working": true,
      "measurements": {
        "time-ms": 0.6165345509847006,
        "estimation": 3.1324,
        "error-percent": 1.2587783174282066
      },
      "alerts": [
        {
          "metric": "time-ms",
          "comparison": ">",
          "value": 1.0
        },
        {
          "metric": "error-percent",
          "comparison": ">",
          "value": 5.0
        }
      ]
    },
    "monte-carlo-pi-10000-samples": {
      "name": "Estimating π with Monte Carlo (10000 samples)",
      "code": "...",
      "working": true,
      "measurements": {
        "time-ms": 6.283108393351237,
        "estimation": 3.1438400000000004,
        "error-percent": 0.34636792486790063
      },
      "alerts": [
        {
          "metric": "time-ms",
          "comparison": ">",
          "value": 10.0
        },
        {
          "metric": "error-percent",
          "comparison": ">",
          "value": 5.0
        }
      ]
    },
    "monte-carlo-pi-100000-samples": {
      "name": "Estimating π with Monte Carlo (100000 samples)",
      "code": "...",
      "working": true,
      "measurements": {
        "time-ms": 59.226385752360024,
        "estimation": 3.1412600000000013,
        "error-percent": 0.1618443357024854
      },
      "alerts": [
        {
          "metric": "time-ms",
          "comparison": ">",
          "value": 100.0
        },
        {
          "metric": "error-percent",
          "comparison": ">",
          "value": 5.0
        }
      ]
    },
    "monte-carlo-pi-1000000-samples": {
      "name": "Estimating π with Monte Carlo (1000000 samples)",
      "code": "...",
      "working": true,
      "measurements": {
        "time-ms": 585.6338977813721,
        "estimation": 3.142038933333333,
        "error-percent": 0.04578153314682254
      },
      "alerts": [
        {
          "metric": "time-ms",
          "comparison": ">",
          "value": 1000.0
        },
        {
          "metric": "error-percent",
          "comparison": ">",
          "value": 5.0
        }
      ]
    }
  }
}
```

This file can be directly sent to the progress tracker backend.

When you run multiple benchmarks one after the other, `progress.json` is extended after each benchmark instead of being overwritten.
This allows you to have multiple benchmark files that you run one after the other to benchmark everything.
To give an example you can execute the following to run clean benchmarks in a directory.

```bash
rm -rf progress.json && for script in benchmarks/*.py; do python $script; done
```

## Customizing the behavior of the library

The behavior of the library can be customized with environment variables.

Here is a list of things that can be customized:
- `PROGRESS_SAMPLES`: Number of samples to make (default: `30`)
- `PROGRESS_OUTPUT`: File to write the JSON output (default `progress.json`)
- `PROGRESS_OUTPUT_INDENT`: Indentaton of the JSON output (for debugging purposes)
- `PROGRESS_MACHINE_NAME`: Name of the machine (to show in the progress tracker)
- `PROGRESS_MACHINE_OS`: Operating system of the machine (to show in the progress tracker)
- `PROGRESS_MACHINE_VCPU`: Number of virtual CPUs of the machine (to show in the progress tracker)

So to sample 5 times and create an indented output, you can do the following.

```bash
PROGRESS_SAMPLES=5 PROGRESS_OUTPUT_INDENT=2 python $script
```
