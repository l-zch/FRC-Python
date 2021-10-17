from wpilib import Victor 

class Storage:

    storageMotor  : Victor

    motor_speed = 0

    def feed(self):
        self.motor_speed = 0.5

    def reverse(self):
        self.motor_speed = -0.5

    def execute(self):
        self.storageMotor.set(self.motor_speed)
        self.motor_speed = 0