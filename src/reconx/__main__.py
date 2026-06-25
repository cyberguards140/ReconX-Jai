from reconx.logger import setup_logger

logger = setup_logger("reconx")


def main():
    try:
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
