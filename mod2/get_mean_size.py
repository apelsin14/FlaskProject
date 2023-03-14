import sys


def get_mean_size(lines):
    summary = 0
    for line in lines:
        summary += int(line.split()[4])
    mean_size = summary //len(lines)
    return f"{mean_size // (2 ** 20)} MB {(mean_size % (2 ** 20)) // 2 ** 10} KB {mean_size % 2 ** 10} B"


if __name__ == '__main__':
    lines = sys.stdin.readlines()[1:]
    print(get_mean_size(lines))
