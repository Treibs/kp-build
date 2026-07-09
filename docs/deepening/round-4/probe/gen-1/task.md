Write a Sui Move module `contest::prize` (edition 2024), generic over the prize type. A sponsor
calls `open_contest`, depositing a prize item of any suitable type; this creates a shared
`Contest` holding the prize and issues the sponsor a `JudgeCap` tied to that contest. When the
contest ends the judge calls `award(contest, winner)`, which takes the prize out of the contest
and delivers it to the winner's address; a contest can only be awarded once (abort on a second
attempt). `is_open` is a public view reporting whether the prize is still unclaimed.
