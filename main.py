import logging
from scrapers.ethiopian_airlines import scrape_ethiopian_airlines
from scrapers.ethiojobs import scrape_ethiojobs
from scrapers.hahujobs import scrape_hahujobs
from utils.supabase_client import upsert_jobs

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    jobs = []
    for name, scraper in [
        ("Ethiopian Airlines", scrape_ethiopian_airlines),
        ("Ethiojobs", scrape_ethiojobs),
        ("HaHuJobs", scrape_hahujobs),
    ]:
        try:
            found = scraper()
            logging.info("%s: %s jobs", name, len(found))
            jobs.extend(found)
        except Exception:
            logging.exception("%s collector failed", name)
    if jobs:
        upsert_jobs(jobs)
    else:
        logging.info("No jobs collected.")

if __name__ == "__main__":
    main()
