import shutil


class Counter:
    """
    Class used to display a progress bar. Rewrites on the same line to get a moving progress bar.
    Prints only if there is a difference with the previous print, not to slow the bigger process.
    The counter can be called, with an integer ``i``. ``i == -1`` correspond to 0% and ``i == n - 1`` to 100%.
    :param str text: The text of the counter
    :param int n: The final value
    Example:
       >>> n_max = 400
       >>> c = Counter('Text', n_max)
       >>> for i in range(-1, n_max):
       ...     c(i)  # Will display a new message only when i = -1, 3, 7, ..., 399 in this example
       >>>
    """

    def __init__(self, text, n, flg=False):
        self.text = text
        self.n = n
        self.i = -1
        if self.text:
            self.string = '{0} - |{{0:<{{bar_length}}}}| {{1:=4.0%}}'.format(self.text)
        else:
            self.string = '|{0:<{bar_length}}| {1:=4.0%}'
        if flg:
            self(-1)

    def __call__(self, i):
        i += 1
        if self.n == 0 or i > self.n or 100 * self.i // self.n == 100 * i // self.n:
            return
        self.i = i
        try:
            bar_length = min(100, shutil.get_terminal_size().columns) + 22 - len(self.string)
        except AttributeError:
            bar_length = 10
        if i > 1:
            print('\033[1A', end='')
        print(self.string.format(int(bar_length * i / self.n) * '-', i / self.n, bar_length=bar_length))
