"""Smoke tests for pydd."""

from pydd import DdException, configure, dump, render_html, render_text


def test_render_html_dict():
    html = render_html({'tags': ['python', 'debug']})
    assert 'dict:1' in html
    assert 'list:2' in html
    assert 'sf-dump-toggle' in html


def test_render_html_multiple_dumps_separated():
    html = render_html({'a': 1}, {'b': 2})
    assert html.count('<pre class=sf-dump>') == 2
    assert 'margin:0 0 1em' in html


def test_render_html_tip_after_arrow():
    html = render_html({'a': 1})
    assert 'sf-dump-arrow' in html
    assert 'sf-dump-tip-in' in html
    assert 'sf-dump-tip-out' in html
    # Expanded: tip-in after arrow, before <samp>
    arrow_idx = html.find('sf-dump-arrow')
    tip_in_idx = html.find('sf-dump-tip-in', arrow_idx)
    samp_idx = html.find('<samp', arrow_idx)
    assert tip_in_idx != -1 and samp_idx != -1
    assert tip_in_idx < samp_idx
    # Collapsed: tip-out after closing ]
    close_idx = html.find('</samp>]')
    tip_out_idx = html.find('sf-dump-tip-out', close_idx)
    assert tip_out_idx != -1


def test_render_text_via_pydump():
    text = render_text({'a': 1}, color=False)
    assert 'dict:1' in text


def test_dump_stderr(capsys):
    dump('hello')
    assert 'hello' in capsys.readouterr().err


def test_dd_exception_payload():
    exc = DdException('<html>x</html>')
    assert exc.html == '<html>x</html>'


def test_configure():
    configure(project_root='.')


def test_dd_boot_mode_no_exit():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from pydd import dd

    app = FastAPI()
    dd(app)
    assert getattr(app, '_pydd_boot_html', None)
    client = TestClient(app, raise_server_exceptions=False)
    r = client.get('/')
    assert r.status_code == 500
    assert 'sf-dump' in r.text


def test_dd_var_outside_request_does_not_arm():
    """FastAPI existing must not hijack dd(var) into boot mode."""
    from fastapi import FastAPI
    import pytest
    from pydd import dd

    app = FastAPI()
    with pytest.raises(SystemExit) as exc:
        dd({'x': 1})
    assert exc.value.code == 1
    assert getattr(app, '_pydd_boot_html', None) is None


def test_builtins_helpers_override_pydump():
    import builtins
    import pytest
    from pydd import dd, dump

    assert builtins.dd is dd
    assert builtins.dump is dump
    dump('via-builtin')
    with pytest.raises(SystemExit):
        builtins.dd({'x': 1})
