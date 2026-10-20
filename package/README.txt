# Pac-Man

Launch
  ./pacman config.json    play with config.json, next to the game
  ./pacman other.json     play with another config file

Controls
  Arrow keys     move
  Space          start a game from the menu
  Left / Right   switch between highscores and controls on the menu
  Escape         pause, Escape again resumes, Enter goes back to the menu
  Q              quit from the menu

Cheats
  I              toggle invincibility
  F              toggle frozen ghosts
  W              clear the level

Configuration
  config.json is a JSON object and every key is optional. A missing file,
  invalid JSON or an out of range value falls back to the defaults below,
  with a warning in the terminal. Unknown keys are ignored.

  key                       default                 allowed
  lives                     3                       1 - 99
  levels_to_win             3                       1 - 99
  level_time_limit          180                     1 - 3600 seconds
  speed                     10.0                    1 - 15 tiles per second
  entity_hitbox             0.5                     0.25 - 1 tile
  cheat_win_key             "w"                     a letter
  cheat_invincible_key      "i"                     a letter
  cheat_freeze_ghosts_key   "f"                     a letter
  highscore_path            "saves/highscore.json"  relative to config.json

Highscores
  The 10 best scores are kept in saves/highscore.json, one per name.
