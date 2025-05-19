# RandomGen – Weighted Random Number Generator

Python implementation of a weighted random number generator that returns values based on user-defined probabilities.


## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vladi2703/RandomGen.git
cd RandomGen 
```

### 2. Install in Editable Mode

This will allow the `src/` code to be used directly without needing to change `PYTHONPATH`.

```bash
pip install -e .
```

### 3. Install Test Dependencies

```bash
pip install -r requirements.txt
```


## Running the Tests

This project uses `pytest` for unit and statistical testing.

```bash
python3 -m unittest
```

Tests include:

* `test_random_gen.py`: Unit tests for constructor validation and sampling
* `test_chi_square.py`: Statistical tests to verify probability distribution over large samples


## Usage

```python
from random_gen import RandomGen

values = [-1, 0, 1, 2, 3]
probs = [0.01, 0.3, 0.58, 0.1, 0.01]

gen = RandomGen(values, probs)
print(gen.next_num())
```

The generator will return values roughly in line with the specified probabilities over time.


## How It Works

* Computes a **cumulative distribution** of the input probabilities
* Uses **binary search** or a **lookup cache** depending on precision needs
