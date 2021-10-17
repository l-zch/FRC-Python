from magicbot import StateMachine, state, timed_state
from .storage import Storage
from .shooter import Shooter

class ShooterController(StateMachine):

    shooter: Shooter
    storage: Storage

    def fire(self):
        '''This function is called from teleop or autonomous to cause the
            shooter to fire'''
        self.engage()

    @state(first=True)
    def prepare_to_fire(self):
        if self.shooter.is_ready():
            self.next_state_now('firing')

    @timed_state(duration=1, must_finish=True)
    def firing(self):
        '''Fires the ball'''
        self.shooter.shoot()
        self.storage.feed()
