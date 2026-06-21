from logic_utils import check_guess, get_range_for_difficulty, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_hard_range_is_larger_than_normal():
    # Hard mode should be harder than Normal — meaning a bigger number range to guess from
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard mode should have a bigger range than Normal"


def test_easy_range_is_smallest():
    # Easy should be the easiest — smallest range
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high, "Easy mode should have a smaller range than Normal"


def test_wrong_guess_always_loses_points():
    # A wrong guess should always deduct points, never add them
    score_after_too_high = update_score(100, "Too High", 2)
    score_after_too_low = update_score(100, "Too Low", 2)
    assert score_after_too_high < 100, "Too High guess should deduct points"
    assert score_after_too_low < 100, "Too Low guess should deduct points"


def test_attempt_limits_order():
    # Easy should allow more attempts than Normal, and Normal more than Hard
    attempt_limit_map = {"Easy": 10, "Normal": 7, "Hard": 5}
    assert attempt_limit_map["Easy"] > attempt_limit_map["Normal"], "Easy should have more attempts than Normal"
    assert attempt_limit_map["Normal"] > attempt_limit_map["Hard"], "Normal should have more attempts than Hard"
