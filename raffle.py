#!/usr/bin/env python3

import random
from typing import NewType, Mapping, Collection, Sequence

Participant = NewType('Participant', str)
Prize = NewType('Prize', str)


def raffle(
        prizes: Sequence[Prize],
        entries: Collection[Participant],
        preferences: Mapping[Participant, Sequence[Prize]],
        random_source: random.Random = random.SystemRandom()) -> Mapping[Participant, Prize]:

    hat = list(entries)
    results = {}

    for prize in prizes:
        winner = hat.pop()
        results[winner] = prize

    return results
