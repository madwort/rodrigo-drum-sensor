from drum_sensor import samples


def test_samples_to_seconds():
    seconds = samples.convert_samples_to_seconds(80)
    assert seconds == 0.0018140589569160999
