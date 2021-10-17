from wpilib import SpeedControllerGroup, PWMVictorSPX, Victor
from wpilib.drive import DifferentialDrive


class DriveTrain:

    frontLeftMotor  : Victor
    rearLeftMotor   : Victor
    frontRightMotor : Victor
    rearRightMotor  : Victor

    def setup(self):
        self.drive = DifferentialDrive(
            SpeedControllerGroup(self.frontLeftMotor,self.rearLeftMotor),
            SpeedControllerGroup(self.frontRightMotor,self.rearRightMotor),
        )

    def on_enable(self):
        self.logger.info(
            "Robot is enabled"
        )

    def on_disable(self):
        self.drive.tankDrive(0,0,True)
        self.logger.info(
            "Robot is disabled"
        )
    
    def move(self, left_motor_speed, right_motor_speed):
        self.left_motor_speed = left_motor_speed
        self.right_motor_speed = right_motor_speed

    def execute(self):
        self.drive.tankDrive(-self.left_motor_speed,-self.right_motor_speed,True)
