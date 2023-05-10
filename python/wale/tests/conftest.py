def pytest_addoption(parser):
    parser.addoption(
        "--api-root",
        action="store",
        default="https://api.trywale.com",
        help="Root URL of the API",
    )
