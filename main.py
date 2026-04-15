# generic imports
from pydantic import BaseModel, field_validator, Field

# local imports
from utils.tools import export_data, format_date
from utils.scraper import Scraper
from utils.consts import STATES


class AffiliatePerformance(BaseModel):
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    code: str
    registration: int = Field(..., ge=0)
    ftds: int = Field(..., ge=0)
    state: str = Field(..., pattern=r'^[A-Z]{2}$')
    
    @field_validator("code")
    def validate_code(cls, value):
        if not value.startswith("AFF"):
            raise ValueError("code must start with AFF")
        return value

    @field_validator("registration")
    def validate_registration(cls, value):
        if value < 0:
            raise ValueError("registration must be non-negative")
        return value

    @field_validator("ftds")
    def validate_ftds(cls, value):
        if value < 0:
            raise ValueError("ftds must be non-negative")
        return value

    @field_validator("state")
    def validate_state(cls, value):
        if value not in STATES:
            raise ValueError("state must be a valid state")
        return value


class AffiliatePerformanceHandler:
    def handle(self):
        scraped_data = Scraper().extract_data()
        performances = []

        for item in scraped_data:
            item["date"] = format_date(item["date"])

            performance = AffiliatePerformance(**item).model_dump(mode="json")
            performances.append(performance)

        export_data(performances)


if __name__ == "__main__":
    handler = AffiliatePerformanceHandler()
    handler.handle()
