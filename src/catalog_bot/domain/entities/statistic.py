from dataclasses import dataclass


@dataclass
class StatisticEntity:
    users_count: int
    in_the_block_count: int
    new_this_month: int
    new_this_day: int
