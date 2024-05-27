import generations_scraper_1 as generations_scraper
import type_scraper_2 as type_scraper
import pokemon_scraper_3 as pokemon_scraper
import moves_scraper_4 as moves_scraper
import evo_scraper_5 as evo_scraper
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    try:
        logging.info("Running generations scraper...")
        generations_scraper.main()
    except Exception as e:
        logging.error(f"Error running generations scraper: {e}")

    try:
        logging.info("Running type scraper...")
        type_scraper.main()
    except Exception as e:
        logging.error(f"Error running type scraper: {e}")

    try:
        logging.info("Running pokemon scraper...")
        pokemon_scraper.main()
    except Exception as e:
        logging.error(f"Error running pokemon scraper: {e}")

    try:
        logging.info("Running moves scraper...")
        moves_scraper.main()
    except Exception as e:
        logging.error(f"Error running moves scraper: {e}")

    try:
        logging.info("Running evolution scraper...")
        evo_scraper.main()
    except Exception as e:
        logging.error(f"Error running evolution scraper: {e}")


if __name__ == "__main__":
    main()
