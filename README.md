# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** A number guessing game where the player picks a difficulty (Easy, Normal, or Hard), then guesses a secret number within a limited number of attempts. Each wrong guess gives a hint (Too High / Too Low) and affects the score. The game ends when the player guesses correctly or runs out of attempts.

- [x] **Bugs found:** 8 bugs were identified across Phase 1 and Phase 2. The three main bugs were reversed hint messages, swapped difficulty ranges between Normal and Hard, and a broken Play Again button. Five additional bugs were found during repair: the secret being cast to a string on even turns breaking comparisons, attempt limits being out of order, the hint text always showing "1 and 100" regardless of difficulty, the attempts counter starting at 1 instead of 0, and the scoring system awarding +5 points for wrong guesses on even turns.

- [x] **Fixes applied:** All four game logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) were refactored from `app.py` into `logic_utils.py` with the bugs corrected. The hint messages were reversed to the correct direction, the string-cast was removed, difficulty ranges were swapped to the correct order, the Play Again button was updated to reset all session state, attempt limits were reordered, and the scoring logic was made consistent. Every fix was labeled with a `# FIX:` comment in the code.

## 📸 Demo Walkthrough

1. Player opens the app and selects **Normal** difficulty from the sidebar. The sidebar shows the range is **1 to 50** and 7 attempts are allowed.
2. Player types **25** and clicks Submit. The game returns **"📈 Go HIGHER!"** — the secret number is above 25.
3. Player types **40** and clicks Submit. The game returns **"📉 Go LOWER!"** — the secret number is below 40.
4. Player types **32** and clicks Submit. The game returns **"📈 Go HIGHER!"** — narrowing in.
5. Player types **36** and clicks Submit. The game returns **"🎉 Correct!"** — balloons appear, the secret number is revealed as 36, and a final score is displayed.
6. Player clicks **New Game**. The score resets to 0, the attempt counter resets, and a fresh secret number is generated within the correct difficulty range.

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.10.2, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Muska\ai110-gameglitch
collecting ... collected 7 items

tests/test_game_logic.py::test_winning_guess                    PASSED [ 14%]
tests/test_game_logic.py::test_guess_too_high                   PASSED [ 28%]
tests/test_game_logic.py::test_guess_too_low                    PASSED [ 42%]
tests/test_game_logic.py::test_hard_range_is_larger_than_normal PASSED [ 57%]
tests/test_game_logic.py::test_easy_range_is_smallest           PASSED [ 71%]
tests/test_game_logic.py::test_wrong_guess_always_loses_points  PASSED [ 85%]
tests/test_game_logic.py::test_attempt_limits_order             PASSED [100%]

============================== 7 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
