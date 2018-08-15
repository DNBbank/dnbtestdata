import random
from datetime import datetime, timedelta
from .card_status import CardStatus

SECONDS_IN_A_YEAR = 31557600

class BlockingInfo:
    @classmethod
    def generate_random(cls, card_status):
        #Generate timestamp falling somewhere in the last 365 days

        random_seconds = random.randint(0, SECONDS_IN_A_YEAR)

        timestamp = ""
        performed_by = ""
        if card_status == CardStatus.BLOCKED:
            random_date = datetime.today() - timedelta(seconds=random_seconds)
            timestamp = random_date.isoformat(sep=" ", timespec="seconds")
            performed_by = random.choice(["B", "C"])


        return  {
            "performedBy": performed_by,
            "timestamp": timestamp,
            "blockAllowed": str(random.choice(["true", "false"])),
            "unblockAllowed": str(random.choice(["true", "false"]))
         }
