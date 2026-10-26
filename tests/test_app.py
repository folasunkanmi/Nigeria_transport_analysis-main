from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_dashboard_and_filters():
    app = AppTest.from_file(str(Path(__file__).parents[1] / 'app.py')).run(timeout=30)
    assert not app.exception
    assert app.metric[0].value == '240'
    app.multiselect[0].select('Bus').run()
    assert not app.exception
    assert int(app.metric[0].value) < 240
    app.multiselect[1].select('Lagos').run()
    assert not app.exception
