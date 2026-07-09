Write a Sui Move module `paywall::access` (edition 2024). A shared `Article` object carries a
title, a price in MIST, and the proceeds collected so far. Anyone can call `unlock`, paying the
exact price in SUI (abort on any other amount); the payment joins the article's proceeds and the
caller receives an owned `AccessPass` object recording the article's title. The author (who holds
an `AuthorCap` issued at creation) can call `collect`, which takes all accumulated proceeds and
returns them to the author as spendable coin.
