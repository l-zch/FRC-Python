from wpilib import Victor

class Shooter:

    leftShooterMotor  : Victor
    rightShooterMotor   : Victor

    motor_speed = 0

    def is_ready(self):
        return True

    def shoot(self):
        self.motor_speed = 0.5

    def execute(self):
        '''This gets called at the end of the control loop'''

        self.leftShooterMotor.set(self.motor_speed)
        self.rightShooterMotor.set(self.motor_speed)
        self.motor_speed = 0