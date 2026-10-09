from enum import IntEnum


class Keys(IntEnum):
    Space = 32
    Return = 65293
    Backspace = 65288
    Escape = 65307
    Left = 65361
    Up = 65362
    Right = 65363
    Down = 65364

    A, B, C, D, E, F, G, H, I, J, K, L, M = range(ord("a"), ord("m") + 1)
    N, O, P, Q, R, S, T, U, V, W, X, Y, Z = range(ord("n"), ord("z") + 1)
