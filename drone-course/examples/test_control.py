"""Các kiểm tra hành vi quan trọng của bộ điều khiển và mixer."""
import unittest

from quad_pid import PID, mixer_x, wrench_x
from sim_cascade import main
from sim_position_hold import main as position_main


class ControlTests(unittest.TestCase):
    def test_derivative_on_measurement_avoids_setpoint_kick(self):
        pid = PID(0.0, 0.0, 1.0, 10.0, 0.0)
        pid.reset(0.0)
        self.assertEqual(pid.update(1.0, 0.0, 0.002), 0.0)

    def test_integral_stops_growing_at_output_limit(self):
        pid = PID(1.0, 5.0, 0.0, 0.5, 10.0)
        pid.reset(0.0)
        for _ in range(1000):
            pid.update(10.0, 0.0, 0.002)
        self.assertAlmostEqual(pid.integral, 0.0)

    def test_mixer_delivers_requested_wrench(self):
        requested = (9.81, (0.02, -0.01, 0.005))
        omega, saturated = mixer_x(*requested, 0.18, 0.02, 1.5e-5, 650.0)
        self.assertFalse(saturated)
        actual = wrench_x(omega, 0.18, 0.02, 1.5e-5)
        self.assertAlmostEqual(actual[0], requested[0], places=8)
        for a, b in zip(actual[1], requested[1]):
            self.assertAlmostEqual(a, b, places=8)

    def test_step_response_returns_near_zero(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as tmp:
            rows = main(Path(tmp) / "step.csv")
        self.assertGreater(next(r[2] for r in rows if r[0] >= 2.4), 8.0)
        self.assertLess(abs(rows[-1][2]), 1.0)

    def test_full_cascade_reaches_position_setpoint(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as tmp:
            rows = position_main(Path(tmp) / "position.csv")
        self.assertLess(abs(rows[-1][2] - 1.0), 0.08)
        self.assertLess(abs(rows[-1][3]), 0.05)
        self.assertLess(abs(rows[-1][4] - 1.0), 0.05)


if __name__ == "__main__":
    unittest.main()
