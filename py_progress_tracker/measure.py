import time

from .state import MEASUREMENTS, METRICS, ALERTS

ALERT_OPERATORS = ["==", "!=", "<=", ">=", "<", ">"]

class measure(object):
    def __init__(self, id, label, value=None, alert=None):
        self.id = id

        METRICS[id] = label
        if id not in MEASUREMENTS:
            MEASUREMENTS[id] = []

        if value is not None:
            MEASUREMENTS[id].append(value)

        if alert is not None:
            alerts = [alert] if not isinstance(alert, list) else alert

            for alert in alerts:
                if not isinstance(alert, tuple) or len(alert) != 2:
                    raise ValueError("Alerts must be of tuple with two elements")

                operator, threshold = alert

                if operator not in ALERT_OPERATORS:
                    raise ValueError(f"Operators must one of {', '.join(ALERT_OPERATORS)}")

                if isinstance(threshold, int):
                    threshold = float(threshold)

                if not isinstance(threshold, float):
                    raise ValueError(f"Threshold must be of type float")

                ALERTS.append(
                    {
                        "metric": id,
                        "comparison": operator,
                        "value": threshold
                    }
                )

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        end = time.time()
        start = self.start

        MEASUREMENTS[self.id].append((end - start) * 1000)
