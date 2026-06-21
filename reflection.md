# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, the interface loaded correctly and allowed me to select a difficulty level and enter guesses. However, after playing several rounds, I noticed that some of the game behavior did not match what I expected. The game appeared functional at first, but several features were either misleading or broken.

Through Phase 1 investigation and Phase 2 repair, a total of **8 bugs** were identified and fixed. The three main bugs were: hint messages being reversed, difficulty ranges being swapped between Normal and Hard, and the Play Again button not properly resetting the game. Five additional bugs were discovered during Phase 2: the secret being converted to a string on even turns breaking comparisons, attempt limits being out of order, the hint text always displaying "1 and 100" regardless of difficulty, the attempt counter initializing to 1 instead of 0, and the scoring system incorrectly awarding points for wrong guesses on even turns.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Enter a guess higher than the secret | Hint should say "Go LOWER!" | Hint said "Go HIGHER!" — message was reversed | None |
| Enter a guess on an even-numbered turn | Hint should compare numbers correctly | Secret was converted to a string, causing wrong comparisons | None |
| Change difficulty from Normal to Hard | Hard mode should have a larger number range | Normal showed 1–100, Hard showed 1–50 — they were swapped | None |
| Click "Play Again" after finishing a game | Game should fully reset and allow new guesses | status, score, and history were not reset; game stayed locked | None |
| Compare attempt limits across difficulties | Easy should allow the most attempts, Hard the fewest | Normal (8) had more attempts than Easy (6) — order was wrong | None |
| Play on Easy mode | Info text should say "Guess between 1 and 20" | Info text always said "Guess between 1 and 100" regardless of difficulty | None |
| Start a brand new game for the first time | Should start with full attempts available | attempts initialized to 1 instead of 0, losing one attempt on first game | None |
| Make a wrong guess on an even-numbered turn | Score should decrease | Score increased by 5 points on even turns for wrong guesses | None |

**Total bugs fixed: 8**

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet 4.6) as my AI coding assistant throughout Phase 2. I asked it to explain the code in plain terms, walk me through each bug step by step, perform the refactor from `app.py` into `logic_utils.py`, write and run tests, and help document the fixes. The AI edited files directly using agent mode, while I reviewed every change, asked follow-up questions, and caught issues the AI missed or described inaccurately.

**Correct AI suggestion:** The AI correctly identified that the `check_guess` function in `app.py` had two separate problems causing wrong hints — the messages were reversed AND the secret was being converted to a string on every even-numbered turn, breaking number comparison entirely. The AI suggested moving a fixed version of `check_guess` into `logic_utils.py` that removed the string-cast, used only integer comparison, and returned just the outcome string (`"Too High"`, `"Too Low"`, `"Win"`) to match the starter tests. I verified this was correct in two ways: first by reading the new function logic myself and confirming `if guess > secret: return "Too High"` is logically sound, and second by running `pytest` which showed `test_guess_too_high` and `test_guess_too_low` both passing.

**Incorrect or misleading AI suggestion:** When the AI first explained the string-cast bug in Phase 1, it described it as a problem that "sometimes causes wrong comparisons." That was misleading — it actually causes wrong comparisons on *every single even-numbered turn*, not just occasionally. The line `if st.session_state.attempts % 2 == 0` runs on turns 2, 4, 6, 8 — meaning exactly half of all guesses in every game were affected. I verified this by carefully reading the condition myself and counting: turn 2 triggers it, turn 3 does not, turn 4 triggers it again — it was a predictable, repeating pattern, not a random or rare one. This taught me that AI explanations can be vague even when the fix itself is correct, and I should always read the code myself rather than just trust the description.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when two things were both true: (1) the code logic visually made sense when I read it myself, and (2) an automated test confirmed the correct output. For UI-related bugs that pytest could not simulate — like the Play Again reset, the attempts counter starting at 0, and the hint text showing the right range — I verified those manually by reading the code logic and tracing through what would happen step by step.

During the session, I asked the AI whether we had written tests for every bug we fixed. The AI mapped each fix against the test file and honestly identified the gaps — the scoring bug and attempt limits bug had no tests yet. We then added `test_wrong_guess_always_loses_points` and `test_attempt_limits_order` to cover those. This showed me that having fixes without tests leaves blind spots, because you cannot automatically confirm those fixes still work if the code changes later.

By the end of the project, the test suite had grown from 3 starter tests to 7 total. Running `python -m pytest tests/test_game_logic.py -v` in the terminal showed all 7 passing. The AI helped me understand why the starter tests expected a single string return value like `"Win"` rather than a tuple — this shaped how we designed `check_guess` in `logic_utils.py` to return just the outcome, keeping the hint messages separate in `app.py`. That separation also made the function much easier to test cleanly.

---

## 4. What did you learn about Streamlit and state?

Imagine you are watching a flip book — every time you press a button, Streamlit throws away the current page and redraws the entire book from the first page again. That full redraw is called a "rerun." Every line of code in `app.py` runs again from top to bottom each time anything happens, like clicking a button or typing in a box.

The problem with reruns is that normal variables get wiped out every time. So Streamlit gives you a special memory box called `session_state` — anything you put in there survives the rerun. That is why the game stores things like `st.session_state.secret`, `st.session_state.attempts`, and `st.session_state.status` instead of plain variables. They need to be remembered across reruns.

The Play Again bug was a perfect example of this. When the New Game button was clicked, it triggered a rerun — but `status` was still sitting in `session_state` as `"won"` or `"lost"`. On the very next rerun, the code checked `status` and immediately called `st.stop()`, freezing the game before the player could do anything. Fixing it meant explicitly resetting `status` back to `"playing"` in the same block where the button was pressed.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is always checking whether every fix has a matching test — not just some of them. During this project I noticed we had fixed several bugs but never wrote tests to confirm them until I specifically asked. Going forward I want to make it a rule: fix a bug, write a test for it immediately, run pytest to confirm. That way there is no guesswork about whether something is actually working.

One thing I would do differently next time is read the code myself before asking the AI to explain it. In this project the AI sometimes gave slightly vague descriptions — like calling the string-cast bug something that "sometimes" causes problems when it actually happened on every even turn. If I had read the code first and formed my own theory, I would have caught that imprecision faster instead of almost accepting it.

AI generated code looks clean and confident, which makes it easy to trust without checking — but this project showed me that it can carry subtle bugs that only appear when you actually play the game or read the logic carefully. I now think of AI as a fast first draft that always needs a human to read, question, and verify before it can be called done.

---
