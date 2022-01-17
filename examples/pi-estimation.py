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
