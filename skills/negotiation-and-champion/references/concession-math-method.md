# Concession math: the method

This file is the exact method for every money figure in this skill. It covers three modes: discount (with any trades the seller asks for in return), multi year and competitor gap. Follow it with your own code execution when it is available, and by hand otherwise, showing the formula. Either way the figures and the printed block must come out the same.

No default price, discount or gap exists in this method. Every figure comes from the user and is shown as "your figures". Nothing is looked up, guessed or filled in.

## 1. Rules that hold in every mode

1. Exact decimal arithmetic. Work in base ten decimals, never in binary floating point (in your own code, use a decimal number type, not a float). Keep full precision until a rounding point named below.
2. Rounding: half up to 2 decimal places. A third decimal of 5 or more moves the second decimal one step away from zero (0.005 becomes 0.01; minus 0.005 becomes minus 0.01). Round only at the points the formulas name.
3. A whole amount carries no decimals (720000, never 720000.00).
4. A missing value is reported as missing, never read as 0.
5. A negative money figure is refused, except the worth of a trade, which keeps its minus sign as a cost.
6. A percentage must be from 0 to 100, both included. Anything else is refused.
7. The first refusal stops the work. Report only that one refusal, in the wording in section 6, and ask for the missing or valid figure.
8. The output block is printed exactly in the shape in section 5: no line merged, shortened, reworded or added.

## 2. Reading a money figure

Applies to the deal value, the annual value and the worth of each trade.

| Step | Rule |
|---|---|
| Missing | Not given is refused (section 6). Never 0. |
| Case and spaces | Read without regard to upper or lower case; ignore spaces at the start and end. |
| Currency | Remove one currency sign or code, at the start or the end: the rupee sign, $, the euro sign, the pound sign, Rs., Rs, INR, USD, EUR, GBP. At the start it may follow a plus or minus sign (minus rupee 500 is minus 500). At the end, a letter code needs a space before it ("500 INR" is read; "500INR" is refused); a symbol does not ("500$" is read). Only one is removed; a second sign or code makes the figure unreadable. |
| Number shape | An optional plus or minus sign, then digits, with commas allowed anywhere before the decimal point, then an optional decimal point with at least one digit after it. "5." is refused; ".5" is read as 0.5. Commas are dropped, so 40,00,000 and 4,000,000 both read as 4000000. |
| Unit word | An optional unit word may follow, with or without a space. Only these are accepted; any other word is refused. |
| Length | More than 30 digits in the typed number (not counting the sign, the commas or the decimal point) is refused. |
| Value | The number times the unit's multiplier. |
| Sign | A result below 0 is refused, except for a trade's worth. |
| Rounding | The result is rounded half up to 2 decimal places, and a whole result keeps no decimals. |

Unit words and multipliers:

| Unit word | Multiplier |
|---|---|
| lakh, lakhs, lac | 100000 |
| crore, crores, cr | 10000000 |
| thousand, k | 1000 |
| million, mn | 1000000 |
| billion, bn | 1000000000 |

Examples: "36 lakh" is 3600000; "Rs 1.2 crore" is 12000000; "250k" is 250000; "1.5 million" is 1500000; "1234567.895" is 1234567.90, shown as 1,234,567.9.

Lakh and crore: the figures are kept as the user typed them in the read back and in the prose. Inside the output block they are printed in plain units (section 4). After the block, restate the key figures in the user's own unit ("7.2 lakh at risk").

## 3. Reading a percentage

Applies to the discount, each yearly discount and the gap.

| Step | Rule |
|---|---|
| Missing | Not given is refused. |
| Shape | Ignore spaces at the start and end and one trailing % sign. Then an optional plus or minus sign, digits, and an optional decimal point with at least one digit after it. No commas, no unit words, no currency. |
| Range | Below 0 or above 100 is refused. A minus percentage is refused, never read as positive. |
| Precision | The percentage is used exactly as typed. It is not rounded. |
| Shown as | Trailing zeros after the decimal point are dropped and a whole number has no decimal point; a leading plus sign or leading zeros are dropped. "20.0%" shows as 20, "12.50" as 12.5, "+5" as 5, ".5" as 0.5. |

## 4. How a money figure is printed

| Case | Printed as |
|---|---|
| Whole amount | Digits grouped in threes with commas, Western style: 3,600,000 (never 36,00,000). |
| Amount with decimals | Grouped in threes, then the decimals with any trailing zero dropped: 1,080,246.90 prints as 1,080,246.9; 154,320.99 stays 154,320.99. |
| Negative amount | A hyphen minus straight before the figure: -15,000. This appears only in a trade's worth or a net that falls below 0. |
| Zero | 0 |

## 5. The three modes

### 5.1 Discount (with trades)

Inputs:

| Input | Rule |
|---|---|
| Deal value (V) | Required. Money figure, not negative. |
| Discount (D) | Required. Percentage 0 to 100. |
| Trades | Optional, in the order the seller gave them. Each one is a label and a worth (written "label=worth"; when there is more than one = sign, the last one splits label from worth). The label is trimmed and must not be empty. The worth is a money figure and may be negative (a cost). Add a trade only when the seller put a worth on it. A trade with no worth is listed after the block as "not priced by you", never as 0. |

Formulas, in this order:

| Figure | Formula | Rounding |
|---|---|---|
| Revenue at risk (R) | V times D, divided by 100 | Round half up to 2 places |
| Value after discount (A) | V minus R (the rounded R) | Round half up to 2 places |
| Net after the trades (N) | A plus the sum of every trade's worth (each worth already rounded when read) | Round half up to 2 places. Only when at least one trade is given. |

Printed block, line by line (braces mark where a figure goes; everything else is printed as written):

| Line | Printed text | When |
|---|---|---|
| 1 | Deal value {V}, discount asked {D}% (your figures). | Always |
| 2 | Revenue at risk: {R} | Always |
| 3 | Value after discount: {A} | Always |
| 4 onward | Trade asked in return: {label}, worth {worth} (your estimate) | One line per trade, in the order given |
| Last | Net after the discount and the trades: {N} | Only when at least one trade is given |

### 5.2 Multi year

Inputs:

| Input | Rule |
|---|---|
| Annual value (V) | Required. Money figure, not negative. |
| Yearly discounts | Required. One percentage per year, separated by commas, year 1 first (for example 0,5,10). An empty list or an empty entry ("5,,6") is refused. Each entry is a percentage 0 to 100. The number of entries is the number of years (Y). |

Formulas:

| Figure | Formula | Rounding |
|---|---|---|
| List price for each year | V | Already rounded when read |
| After discount for year n (Pn) | V minus (V times the year's discount, divided by 100) | Round half up to 2 places once, on the result. The discount amount is not rounded first. |
| Total at list (TL) | V times Y | Round half up to 2 places |
| Total after discounts (TA) | The sum of the rounded Pn | Round half up to 2 places |
| Given up over the term (G) | TL minus TA | Round half up to 2 places |

Note the difference from the discount mode: there the amount at risk is rounded first and then taken off; here the year's price is rounded once at the end. In rare cases the two give a different last cent. Example: a value of 1 at 0.5 percent gives 0.99 after the discount in the discount mode, and 1 after in the multi year mode. Follow each mode as written.

Printed block:

| Line | Printed text | When |
|---|---|---|
| 1 | Annual value {V} over {Y} years (your figures). | Always ("years" even when Y is 1) |
| 2 onward | Year {n}: {V} at list, {discount for year n}% off, {Pn} after | One line per year, year 1 first |
| Then | Total at list: {TL} | Always |
| Then | Total after discounts: {TA} | Always |
| Last | Given up over the term: {G} | Always |

### 5.3 Competitor gap

Use only the gap the buyer stated, as the user reported it. Never look up or guess a competitor's price.

Inputs:

| Input | Rule |
|---|---|
| Deal value (V) | Required. Money figure, not negative. |
| Gap (P) | Required. The percentage the buyer said the other offer is lower, 0 to 100. |

Formulas:

| Figure | Formula | Rounding |
|---|---|---|
| Gap amount (GA) | V times P, divided by 100 | Round half up to 2 places |
| The other offer if the gap holds (O) | V minus GA (the rounded GA) | Round half up to 2 places |

Printed block:

| Line | Printed text |
|---|---|
| 1 | Deal value {V}; the buyer says the other offer is {P}% lower (your figures, not checked). |
| 2 | Gap amount: {GA} |
| 3 | The other offer if that gap holds: {O} |

### 5.4 Amounts, target prices and stacked discounts

The method takes a percentage, never an amount off or a target price. When the buyer's ask is "5 lakh off" or "they offered 30 lakh", ask the user for the percentage or confirm one you read back. For a further discount on top of an earlier one, ask whether it applies to the list price or the discounted price and whether the first is agreed, then run the discount mode on the combined percentage the user confirms.

## 6. Refusals

A refusal is one line that starts with "BAD INPUT: ". Nothing else is printed. Pass it on as written and ask for the figure. The text after the prefix, with the field name filled in:

| Case | Wording after "BAD INPUT: " |
|---|---|
| Deal value missing, discount mode | deal value not given (it is never read as 0) |
| Any other money figure missing | {field} not given: it is reported missing, never read as 0 |
| Money figure unreadable | {field} must be a number (for example 4000000, 40,00,000, 40 lakh or 1.5 million), got '{as typed}' |
| Money figure too long | {field} has more than 30 digits; check the figure, got '{as typed}' |
| Money figure negative | {field} cannot be negative, got {as typed} (the minus sign is kept and refused, never dropped) |
| Percentage missing | {field} not given |
| Percentage unreadable | {field} must be a percentage from 0 to 100, got '{as typed}' |
| Percentage out of range | {field} must be from 0 to 100, got {as typed} |
| Trade without a worth | a trade must be written label=worth, for example "three year term=150000", got '{as typed}' |
| Trade without a label | a trade needs a label before the = sign, got '{as typed}' |
| Yearly discounts empty or with a gap | the yearly discounts must list one percentage per year separated by commas, got '{as typed}' |
| Gap missing | competitor gap not given: type the gap the buyer told you as a percentage (it is never looked up or guessed) |

Field names: "the deal value", "the annual value", "the worth of '{label}'", "the discount", "the discount for year {n}", "the gap".

Order of checks: discount mode reads the deal value, then the discount, then each trade in order. Multi year reads the annual value, then the list of discounts, then each year in order. Gap mode reads the deal value, then the gap.

## 7. Structured form (for API or programmatic use)

When a caller wants data instead of text, give the same figures as JSON, one space of indent, keys in this order. A whole amount is written as a whole number, any other as a decimal number. Characters outside plain ASCII in a label are written as \u escapes.

| Mode | Keys, in order |
|---|---|
| Discount | value, discount_percent, revenue_at_risk, value_after_discount, trades (a list of objects with trade and worth), net_after_trades (null when there are no trades), label |
| Multi year | annual, years, by_year (a list of objects with year, list, discount_percent, after), total_at_list, total_after, given_up, label |
| Gap | value, gap_percent, gap_amount, competitor_price_if_gap_holds, label |

The label values, word for word:

| Mode | label |
|---|---|
| Discount | your figures; the worth of each trade is the value you put on it |
| Multi year | your figures |
| Gap | your figures; the gap is what the buyer said, not checked |

## 8. Worked checks

Use these to confirm your own calculation before you trust it. Each one was produced by the original calculation and must come out identical.

Discount, deal value 36 lakh, 20 percent, one trade "two year term" worth 3 lakh:

| Line | Printed text |
|---|---|
| 1 | Deal value 3,600,000, discount asked 20% (your figures). |
| 2 | Revenue at risk: 720,000 |
| 3 | Value after discount: 2,880,000 |
| 4 | Trade asked in return: two year term, worth 300,000 (your estimate) |
| 5 | Net after the discount and the trades: 3,180,000 |

Working: 3600000 times 20 is 72000000, divided by 100 is 720000 at risk; 3600000 less 720000 is 2880000; 2880000 plus 300000 is 3180000.

Discount with decimals and a cost trade, deal value 1234567.89, 12.50 percent, trades "upfront" worth minus 15,000 and "case study" worth Rs 0.5 lakh:

| Line | Printed text |
|---|---|
| 1 | Deal value 1,234,567.89, discount asked 12.5% (your figures). |
| 2 | Revenue at risk: 154,320.99 |
| 3 | Value after discount: 1,080,246.9 |
| 4 | Trade asked in return: upfront, worth -15,000 (your estimate) |
| 5 | Trade asked in return: case study, worth 50,000 (your estimate) |
| 6 | Net after the discount and the trades: 1,115,246.9 |

Working: 1234567.89 times 12.5 divided by 100 is 154320.98625, rounded half up to 154320.99; 1234567.89 less 154320.99 is 1080246.90; 1080246.90 less 15000 plus 50000 is 1115246.90.

Multi year, annual value 10 lakh, discounts 0,5,10:

| Line | Printed text |
|---|---|
| 1 | Annual value 1,000,000 over 3 years (your figures). |
| 2 | Year 1: 1,000,000 at list, 0% off, 1,000,000 after |
| 3 | Year 2: 1,000,000 at list, 5% off, 950,000 after |
| 4 | Year 3: 1,000,000 at list, 10% off, 900,000 after |
| 5 | Total at list: 3,000,000 |
| 6 | Total after discounts: 2,850,000 |
| 7 | Given up over the term: 150,000 |

Gap, deal value 1.2 crore, gap 30%:

| Line | Printed text |
|---|---|
| 1 | Deal value 12,000,000; the buyer says the other offer is 30% lower (your figures, not checked). |
| 2 | Gap amount: 3,600,000 |
| 3 | The other offer if that gap holds: 8,400,000 |

Refusals: "500inr" as a deal value gives "BAD INPUT: the deal value must be a number (for example 4000000, 40,00,000, 40 lakh or 1.5 million), got '500inr'". "-5 lakh" gives "BAD INPUT: the deal value cannot be negative, got -5 lakh (the minus sign is kept and refused, never dropped)". A discount of 101 gives "BAD INPUT: the discount must be from 0 to 100, got 101".

## 9. By hand

Without code execution, say "worked out by hand per the method", show each formula in words with the user's figures ("60 lakh times 10% is 6 lakh at risk; 60 lakh minus 6 lakh is 54 lakh"), follow the rounding points above, and ask the user to check the arithmetic. SKILL.md, Platform mode, sets which figures to work out in this case and how to write them.
