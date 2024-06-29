from app import app


def main():
    from config import Config

    config = Config()
    app.config.from_object(config)
    app.run(debug=True)


if __name__ == "__main__":
    main()
