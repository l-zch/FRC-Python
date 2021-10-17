from wpilib.simulation import (
    PWMSim,
    DifferentialDrivetrainSim,
    EncoderSim,
    AnalogGyroSim,
)
from wpilib import RobotController
from wpimath.geometry import Transform2d
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor
from pyfrc.physics import drivetrains
from pyfrc.physics.visionsim import VisionSim, VisionSimTarget
from networktables.util import ntproperty


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    # array of (found, timestamp, angle)
    target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))

    def __init__(self, physics_controller):
        """
        :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                   to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.position = 0

        targets = [
            # right
            VisionSimTarget(15, 13, 250, 0),
            # middle
            VisionSimTarget(16.5, 15.5, 295, 65),
            # left
            VisionSimTarget(15, 18, 0, 110),
        ]

        self.vision = VisionSim(
            targets, 61.0, 1.5, 15, 15, physics_controller=physics_controller
        )

        # Create the motors.
        self.l_motor = PWMSim(2)
        self.r_motor = PWMSim(4)

        self.gyroSim = AnalogGyroSim(0)

        self.system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
        self.drivesim = DifferentialDrivetrainSim(
            self.system,
            0.762,
            DCMotor.CIM(2),
            8,
            0.0508,
        )

    def update_sim(self, now, tm_diff):
        """
        :param now: 目前的時間
        :param tm_diff: 更新狀態的週期
        """
        l_speed = self.l_motor.getSpeed()
        r_speed = self.r_motor.getSpeed()
        voltage = RobotController.getInputVoltage()

        self.drivesim.setInputs(l_speed * voltage, r_speed * voltage)
        self.drivesim.update(tm_diff) # 使用預設值



        self.physics_controller.field.setRobotPose(self.drivesim.getPose())

        pose = self.drivesim.getPose()

        currentTranslation = pose.translation()
        currentRotation = pose.rotation()

        x = currentTranslation.X()
        y = currentTranslation.Y()

        angle = currentRotation.degrees()

        data = self.vision.compute(now, x, y, angle)

        if data is not None:
            self.target = data[0][:3]