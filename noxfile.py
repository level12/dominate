from pathlib import Path

import nox


package_path = Path.cwd()
nox.options.default_venv_backend = 'uv'


def latest_dist():
    files = sorted(Path('./dist').glob('dominate*.tar.gz'))
    return files[-1].resolve()


@nox.session
def build_and_test(session: nox.Session):
    session.run('uv', 'sync', '--active', '--no-dev', '--group', 'tests')
    session.run('python', '-m', 'build', '--no-isolation')
    session.run('uv', 'pip', 'install', latest_dist())
    session.run(
        'pytest',
        '-ra',
        '--tb=native',
        '--strict-markers',
        '--cov=dominate',
        '--cov-config=.github/workflows/.coveragerc',
        '--no-cov-on-fail',
        *session.posargs,
    )
