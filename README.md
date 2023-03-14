# Population upgrade for Thehunter: Call of the walid

Based on deca:https://github.com/kk49/deca and https://github.com/Zhouzp2115/cotw-population-mod

## Project goal

Turn your luck around, or better, force your luck by modifying your population files.

The goal of this script is to modify your population files so all your maps have at least one diamond of each species. If a particular animal type has a great one implemented, you will have a great one. Maybe/probably a diamond too.

It's up to you to find them[^1].

## Usage

**As ~~often~~always, consider running this in a virtual environment.**

I tested using VSCode on Windows 11. your mileage may vary should you try a different setup.

1. install dependencies `pip install -r requirements.txt`
2. copy your population files into the `data` folder
3. run `python .\upgrade_population.py`
4. copy the modified population files back into your game folder. A backup of the original files is made in the `data` folder.

## Status

This project is far from finished. Currently, it is more a proof of concept than a working script.

[^1]: There are different levels of cheating in theHunter Call of the Wild. You have the animal population scanner which is cheating at a low level. Modifying your population file certainly is mid-level. Using [this](http://mathartbang.com/deca/hp/map.html?r=r0) is taking away the fun, unless you're grinding for a diamond scrub hare.