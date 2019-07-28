# Random Priority Raffle

This program implements the **Random Priority** algorithm for assigning `n` objects to `n` participants in a way that is [fair](https://en.wikipedia.org/wiki/Fair_random_assignment) (equal treatment of equals) and [strategyproof](https://en.wikipedia.org/wiki/Strategyproofness) (participants cannot "game the system").

## Usage

1. Make sure you have [Python 3.x](https://www.python.org/downloads/) installed
2. Install dependencies with `pip install -r requirements.txt`
3. Create a YAML configuration file with input parameters (see [config.sample.yaml](./config.sample.yaml) as an example)
4. Run `./random-priority-raffle.py <CONFIG_FILE_PATH>`

## Academic References 
The implementation is based on the following published research:
- Bogomolnaia, Anna; Moulin, Hervé (2001). "A New Solution to the Random Assignment Problem". Journal of Economic Theory. 100 (2): 295. [doi:10.1006/jeth.2000.2710](https://doi.org/10.1006/jeth.2000.2710)
- Abdulkadiroglu, Atila; Sonmez, Tayfun (1998). "Random Serial Dictatorship and the Core from Random Endowments in House Allocation Problems". Econometrica. 66 (3): 689. [doi:10.2307/2998580](https://doi.org/10.2307%2F2998580). JSTOR [2998580](https://www.jstor.org/stable/2998580)

## TODO

- [ ] Write a "how it works" section for the README
