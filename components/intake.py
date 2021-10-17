from wpilib import Victor


class Intake:

    intakeMotor  : Victor

    motor_speed = 0

    def take(self):
        self.motor_speed = 0.5

    def reverse(self):
        self.motor_speed = -0.5

    def execute(self):
        self.intakeMotor.set(self.motor_speed)
        self.motor_speed = 0
