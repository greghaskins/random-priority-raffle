#!/usr/bin/env python3

import random
from typing import NewType, Mapping, Sequence

Email = NewType('Email', str)
Prize = NewType('Prize', str)


def raffle(
        prizes: Sequence[Prize],
        entries: Sequence[Email],
        preferences: Mapping[Email, Sequence[Prize]],
        random_source: random.Random = random.SystemRandom()) -> Mapping[Email, Prize]:
    
    results = {}



    return results


