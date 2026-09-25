## ▶️ Play the Game (Windows)

1. Download `dist.zip` from the [Releases](https://github.com/Kiran8620/AlienInvasion/releases) page
2. Extract the dist.zip
3. Double-click `AlienInvasion.exe` to launch — no installation needed
4. If Windows shows a "Windows protected your PC" SmartScreen warning, click **More info** → **Run anyway** (this appears because the app isn't code-signed, not because anything is wrong)
5. Press **Enter** or click **Play** to start!


# 👾 Alien Invasion

A classic top-down space shooter built with **Python** and **Pygame** — hold off the alien fleet, rack up your score, and survive as many levels as you can. Featuring a fully animated parallax space background with drifting planets, spinning asteroids, and a twinkling starfield.

---

## ✨ Features

- **Classic arcade shooting action** — pilot your ship, blast down waves of aliens, and survive as long as you can
- **Escalating difficulty** — ship speed, bullet speed, alien speed, and alien point values all ramp up as you clear each fleet
- **Persistent high score** — your best score is saved to disk and survives closing/reopening the game, until you choose to reset it
- **Lives shown as hearts** — a clean heart-based life counter instead of plain numbers
- **Pause & resume anytime** — pause the action mid-game with its own sound cue
- **Full sound design** — laser fire, explosions, ship hits, and menu sounds, plus a looping background music track (with an in-game mute toggle)
- **Dynamic space background**
  - Two-layer parallax starfield with subtle twinkling stars
  - Drifting planets and tumbling asteroids in the background, each spawning and scaling randomly
  - Distance-based blur — smaller/farther background objects blur more than closer ones
  - Motion blur trails on fast-spinning asteroids for a genuine sense of motion
- **Score & level tracking** — score, current level, and all-time high score displayed live during play

---

## 🎮 How to Play

### Objective
Destroy the entire fleet of aliens before they either reach the bottom of the screen or collide with your ship. Clear a wave to advance to the next level — every level is faster and harder than the last.

### Controls

| Action | Key |
|---|---|
| Move ship left | `A` or `←` |
| Move ship right | `D` or `→` |
| Fire bullet | `Space` |
| Start game | `Enter` (or click the **Play** button) |
| Pause / Resume | `Enter` (while playing), or click the **Pause** button |
| Mute / unmute music | `M` |
| Reset high score | `Backspace` |
| Quit game | `Q` or `Esc` |

### Tips
- You have 3 lives (hearts) — losing all of them ends the game
- Bullets are limited on screen at once, so time your shots
- The fleet speeds up and bullet allowance increases every time you clear a full wave — stay sharp as levels climb!

---

## 🚀 Running from Source

**Requirements:** Python 3.8+ and pip

```bash
git clone https://github.com/Kiran8620/AlienInvasion.git
cd AlienInvasion
pip install -r requirements.txt
python alien_invasion.py
```

## 📦 Building a Standalone Executable (Windows)

A ready-to-use build script is included:

```bash
build_windows.bat
```

This installs [PyInstaller](https://pyinstaller.org/) and packages the game (including all images and sounds) into a single `AlienInvasion.exe`, found afterward in the `dist/` folder — no Python installation required to run it.

---

## 🗂 Project Structure

```
AlienInvasion/
├── alien_invasion.py      # Main game loop and event handling
├── alien.py                # Alien sprite behavior
├── ship.py                  # Player ship behavior
├── bullet.py                # Bullet sprite behavior
├── button.py                # Play/Pause button UI
├── scoreboard.py            # Score, level, high score, and lives display
├── game_stats.py             # Game state tracking + persistent high score
├── settings.py               # All tunable game settings
├── sound_manager.py          # Sound effects and music playback
├── starfield.py               # Parallax twinkling starfield
├── space_decor.py             # Planets & asteroids background objects
├── space_decor_images.py      # Image paths for background decor
├── depth_blur.py               # Distance-based blur effect
├── motion_blur.py               # Motion trail effect for spinning objects
├── images/                       # Game art assets
├── sounds/                        # Sound effects and music
└── requirements.txt
```

---

## 🙌 Credits

Music by [MondaMusic](https://pixabay.com/users/mondamusic-54713575/) from [Pixabay](https://pixabay.com/)

---

## 📄 License

This project is free to use, modify, and share for personal or educational purposes.
