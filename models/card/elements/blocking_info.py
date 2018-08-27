import random
from datetime import datetime, timedelta
from .card_status import CardStatus
from .card_type import CardType


SECONDS_IN_A_YEAR = 31557600

class BlockingInfo:
    @classmethod
    def generate_random(cls, card_status, card_type):
        #Generate timestamp falling somewhere in the last 365 days
        random_seconds = random.randint(0, SECONDS_IN_A_YEAR)

        timestamp = "null"
        performed_by = ""

        if card_status == CardStatus.BLOCKED:
            random_date = datetime.today() - timedelta(seconds=random_seconds)
            timestamp = random_date.isoformat(sep=" ", timespec="seconds")
            performed_by = random.choice(["B", "C"])

            # Unblocking credit cards is never allowed
        unblock_allowed = "false" if card_type == CardType.CREDIT else str(random.choice(["true", "false"]))
        block_allowed = str(random.choice(["true", "false"]))

        if (card_status == CardStatus.NOTACTIVE):
            unblock_allowed = "false"
            block_allowed = "false"


        return  {
            "performedBy": performed_by,
            "timestamp": timestamp,
            "blockAllowed": block_allowed,
            "unblockAllowed": unblock_allowed
            }
