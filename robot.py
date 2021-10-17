from wpilib import (
    Victor, XboxController, run
)
from wpilib.command import POVButton, JoystickButton
from magicbot import MagicRobot
from components import (
    DriveTrain,
    Intake,
    Shooter,
    ShooterController,
    Storage
)


class MyRobot(MagicRobot):

    driveTrain : DriveTrain
    shooter    : Shooter
    intake     : Intake
    storage    : Storage

    shooterController : ShooterController

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""
        self.controller = XboxController(0)
        self.intakePOSButton  = POVButton(self.controller,0)
        self.intakeNEGButton  = POVButton(self.controller,180)
        self.storagePOSButton = POVButton(self.controller,90)
        self.storageNEGButton = POVButton(self.controller,270)
        self.shooterButton    = JoystickButton(
                self.controller, XboxController.Button.kY.value
            )

        # DriveTrain
        self.frontLeftMotor  = Victor(2)
        self.rearLeftMotor   = Victor(3)
        self.frontRightMotor = Victor(4)
        self.rearRightMotor  = Victor(5)

        # Shooter
        self.leftShooterMotor  = Victor(6)
        self.rightShooterMotor = Victor(7)

        # Intake
        self.intakeMotor = Victor(8)

        # Storage
        self.storageMotor = Victor(9)

    def teleopPeriodic(self):
        leftStick = self.controller.Hand.kLeftHand
        rightStick = self.controller.Hand.kRightHand
        self.driveTrain.move(*map(self.controller.getY,(leftStick, rightStick)))

        if self.shooterButton.get(): self.shooterController.fire()
        if self.intakePOSButton.get(): self.intake.take()
        elif self.intakeNEGButton.get(): self.intake.reverse()
        if self.storagePOSButton.get(): self.storage.feed()
        elif self.storageNEGButton.get() :self.storage.reverse()


if __name__ == "__main__":
    run(MyRobot)

    