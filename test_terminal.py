import pytest
from terminal import MyTerminal
from zipfile import ZipFile
from window_mode import Window


@pytest.fixture
def terminal():
    fs_path = 'my_zip_tes.zip'
    t = MyTerminal(ZipFile(fs_path, 'a'))
    return t


@pytest.fixture
def empty_terminal():
    return MyTerminal(None)


def test_init_1(terminal):
    assert terminal.window is None


def test_init_2(terminal):
    assert terminal.fs is not None


def test_init_3(empty_terminal):
    assert empty_terminal.fs is None


def test_attach_1(empty_terminal):
    assert empty_terminal.window is None


def test_attach_2(terminal):
    terminal.attach(Window(terminal))
    assert terminal.window is not None


def test_start_polling_1(terminal):
    terminal.start_polling()
    assert terminal.polling


def test_cd_1(terminal):
    assert terminal.cd([]) == ''


def test_cd_2(terminal):
    assert terminal.cd(['desktop/..']) == ''


def test_cd_3(terminal):
    assert terminal.cd(['desktop']) == 'desktop/'


def test_ls_1(terminal):
    assert terminal.ls([]) == """1
desktop
hello
img.png
my.txt
user"""


def test_ls_2(terminal):
    terminal.cd('user')
    assert terminal.ls([]) == """me
secrets.txt
top_secret.txt"""


def test_ls_3(terminal):
    assert terminal.ls(['user']) == """me
secrets.txt
top_secret.txt"""


def test_cat_1(terminal):
    assert terminal.cat('1') == ''


def test_cat_2(terminal):
    assert terminal.cat('user/secrets.txt') == """я программирую на python
а ещё на Джаве
а ещё на cc++"""


def test_cat_3(terminal):
    terminal.cd('user')
    assert terminal.cat('secrets.txt') == """я программирую на python
а ещё на Джаве
а ещё на cc++"""
