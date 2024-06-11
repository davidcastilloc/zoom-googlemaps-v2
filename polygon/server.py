from polygon.app import app


def main():
    from polygon.config import Config

    config = Config()
    app.config.from_object(config)
    app.run()


if __name__ == "__main__":
    main()
