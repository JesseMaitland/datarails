import pytest

from datarails.contexts import DataBox
from datarails.runner import DataRailsStepRunner
from datarails.step import DataRailsStep


class MockStep(DataRailsStep):
    def step_one(self):
        pass

    def step_two(self):
        pass


class MockAnotherStep(DataRailsStep):
    def step_one(self):
        pass

    def step_two(self):
        pass


@pytest.fixture
def test_runner_instance():
    steps = [MockStep, MockAnotherStep]
    return DataRailsStepRunner(steps)


def test_constructor(test_runner_instance):
    assert isinstance(test_runner_instance.dbx, DataBox)
    assert isinstance(test_runner_instance._i, int)
    assert test_runner_instance._i == 0
    assert len(test_runner_instance.steps) == 2


def test_reset(test_runner_instance):
    test_runner_instance._i = 1  # Modify the iterator index
    test_runner_instance.reset()
    assert test_runner_instance._i == 0  # Iterator index should be reset to 0


def test_advance(test_runner_instance, capsys):
    # Test that advance increments the _i attribute
    test_runner_instance.reset()
    assert test_runner_instance._i == 0
    test_runner_instance.advance()  # Run first step
    assert test_runner_instance._i == 1

    # Test that advance prints "Running step: 0 : StepInstance" after first step
    captured = capsys.readouterr()
    assert "Running step: 0 : MockStep" in captured.out

    # Test that advance prints "Running step: 1 : StepInstance" after second step
    test_runner_instance.advance()  # Run second step
    captured = capsys.readouterr()
    assert "Running step: 1 : MockAnotherStep" in captured.out

    # Test that advance prints "All Steps Completed." when no more steps
    test_runner_instance.advance()  # Should print "All Steps Completed."
    captured = capsys.readouterr()
    assert "All Steps Completed." in captured.out


def test_get_current_step(test_runner_instance):
    test_runner_instance.reset()
    current_step = test_runner_instance.get_current_step()
    assert isinstance(current_step, MockStep)

    test_runner_instance.advance()
    current_step = test_runner_instance.get_current_step()
    assert isinstance(current_step, MockAnotherStep)
