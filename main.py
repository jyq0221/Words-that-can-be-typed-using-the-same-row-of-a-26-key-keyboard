"""
使用 QWERTY 键盘三行字母统计哪些英文单词可以只用同一行键入。
通过 `wordfreq` 获取 50 万以上的英文词表后筛选结果。
"""
from __future__ import annotations

import re
from wordfreq import top_n_list

# QWERTY 键盘的三行字母
KEYBOARD_ROWS = [
    set("qwertyuiop"),
    set("asdfghjkl"),
    set("zxcvbnm"),
]

LETTER_PATTERN = re.compile(r"^[a-z]+$")


def is_single_row_word(word: str) -> bool:
    """判断单词是否只使用同一行键盘字母。"""
    word = word.lower()
    # 确保只包含 a-z 的字母
    if not LETTER_PATTERN.match(word):
        return False

    matching_rows = [row for row in KEYBOARD_ROWS if set(word).issubset(row)]
    return bool(matching_rows)


def main() -> None:
    # 请求不少于 60 万条的词表，保证覆盖 50 万需求
    raw_words = top_n_list("en", 600_000)
    # 只保留由 a-z 组成的单词
    words = [word.lower() for word in raw_words if LETTER_PATTERN.match(word.lower())]

    single_row_words = [word for word in words if is_single_row_word(word)]

    count_single_row = len(single_row_words)
    total_words = len(words)
    proportion = count_single_row / total_words if total_words else 0

    longest_length = max((len(word) for word in single_row_words), default=0)
    longest_words = sorted({word for word in single_row_words if len(word) == longest_length})

    print("Total words analyzed:", total_words)
    print("Words typed with one keyboard row:", count_single_row)
    print("Proportion:", f"{proportion:.6f}")
    print("Longest length:", longest_length)
    print("Words with that length:")
    for word in longest_words:
        print(word)


if __name__ == "__main__":
    main()
