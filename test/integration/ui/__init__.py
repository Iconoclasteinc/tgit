from tgit.ui.main_window import StyleSheet

SIZE = (1100, 745)


def show_widget(driver, widget):
    widget.setStyleSheet(StyleSheet)
    widget.setFixedSize(*SIZE)
    driver.show()


# noinspection PyUnusedLocal
def ignore(*args, **kwargs):
    pass
