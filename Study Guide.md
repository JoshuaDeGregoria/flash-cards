# Study Guide: Inflation, CPI, Money, and Banking

This document reorganizes the quiz material into a clean study guide. It focuses on the main concepts, formulas, and patterns that showed up repeatedly in the original notes.

## 1. Inflation

### What inflation means

- Inflation is a sustained increase in the overall price level.
- A rise in the price of one good does not automatically mean inflation.
- If all prices rise together, that is inflation.
- If only one good becomes more expensive because demand rises or supply falls, that is a relative price change.

### Why inflation matters

- High and unstable inflation makes long-term planning harder.
- Inflation reduces the purchasing power of money.
- Hyperinflation means prices rise extremely fast and money loses value very quickly.
- Deflation means the overall price level falls.

### Who gains and who loses from inflation

Unexpected inflation usually:

- Helps borrowers because they repay loans with dollars worth less than expected.
- Helps employers when wages are fixed in nominal terms.
- Hurts lenders.
- Hurts workers or savers who receive fixed nominal payments.

Unexpected deflation usually:

- Hurts people with debts because the real burden of debt rises.
- Can hurt business owners because revenues may fall.

### Shoe-leather costs

- "Shoe-leather costs" are the extra costs people face when they try to avoid holding cash during inflation.
- Example: moving wealth into gold or other assets because you expect high inflation.

### Key formula: real interest rate

Approximation:

```text
Real interest rate = nominal interest rate - expected inflation
```

More exact version:

```text
Real interest rate = ((1 + nominal rate) / (1 + inflation rate)) - 1
```

Example:

- Nominal return = 6.45%
- Expected inflation = 3.48%
- Real interest rate = about 2.87%

### Key formula: required nominal growth for a target real increase

If you want purchasing power to rise by a certain percentage, use:

```text
(1 + nominal growth) = (1 + real growth) x (1 + inflation)
```

So:

```text
Nominal growth = (1 + real growth)(1 + inflation) - 1
```

Example:

- Desired real increase = 5.79%
- Expected inflation = 1.21%
- Required nominal increase = about 7.07%

## 2. Consumer Price Index (CPI) and Indexing

### What the CPI measures

- CPI measures the cost of a standard basket of goods and services in one year relative to the cost of the same basket in a base year.
- In the base year, CPI = 100 if the index is written in the common 100-based format.

### Steps to calculate CPI

1. Choose a base year.
2. List the goods and services in the typical basket.
3. Calculate the cost of that basket in the base year.
4. Calculate the cost of the same basket in the current year.
5. Divide current basket cost by base-year basket cost.
6. Multiply by 100.

### CPI formula

```text
CPI = (Cost of basket today / Cost of basket in base year) x 100
```

Example:

- Base-year cost of living = $51,963
- Current cost of living = $63,026
- CPI = 121.30

### Inflation rate formula

```text
Inflation rate = ((CPI this year - CPI last year) / CPI last year) x 100%
```

Example:

- Last year CPI = 101.2
- This year CPI = 104.4
- Inflation rate = 3.16%

### Inflation-adjusted or "real" values

To convert a nominal value into base-year dollars:

```text
Real value = (Nominal value / Price index) x 100
```

If you are comparing two years directly:

```text
Equivalent value in target year = Value in original year x (Target CPI / Original CPI)
```

### Important CPI ideas

- In the base year, the inflation-adjusted quantity equals the nominal quantity.
- If prices have risen over time, a nominal value from a later year becomes smaller when adjusted back to the base year.
- If prices have risen over time, a nominal value from an earlier year becomes larger when adjusted forward to a later year.

### Example: wage adjustment

- Wage in February 2020 = $23.96
- CPI in February 2020 = 259.050
- CPI in July 1983 = 100
- Equivalent wage in 1983 dollars = about $9.25

## 3. Real vs. Nominal Values

### Nominal values

- Measured in current dollars.
- Not adjusted for inflation.

Examples:

- Current wages
- Current price of oil
- Current dollar value of income

### Real values

- Adjusted for inflation.
- Measured in purchasing power rather than raw dollars.

Examples:

- Inflation-adjusted wages
- Real interest rate
- Output measured in physical units, such as tons of steel

### Quick rule

- Use nominal values to describe dollar amounts.
- Use real values to compare purchasing power across time.

## 4. Money and the Financial System

### The three functions of money

- **Medium of exchange**: used to buy goods and services.
- **Unit of account**: measures value in a common unit, such as dollars.
- **Store of value**: holds wealth over time.

### What money is

- Money is any asset that people generally accept in payment for goods and services.
- Money is not limited to bills and coins.
- Bank deposits are a major part of the money supply.

### What banks do

Banks help the economy by:

- Transferring funds from savers to borrowers.
- Collecting and using information about borrowers.
- Supporting the payment system.
- Making investment and production possible by channeling funds to productive uses.

### Liquidity

- Liquidity is the ease with which an asset can be exchanged for goods and services.
- The more easily it can be used as payment, the more liquid it is.

Typical liquidity ranking:

1. Bills and coins
2. Checking accounts
3. Savings accounts
4. Short-term certificates of deposit
5. Long-term certificates of deposit
6. Housing

### M1 and M2

- **M1** is the most liquid money.
- **M2** includes all of M1 plus less-liquid assets such as savings deposits and small time deposits.
- M2 includes all components of M1.
- In the United States, deposits make up most of the money supply.

## 5. Banking, Reserves, and Money Creation

### Key definitions

- **Monetary base** = currency + bank reserves
- **Money supply** = currency held by the public + deposits
- **Reserve-deposit ratio** = reserves / deposits

### Basic bank balance intuition

When a bank receives deposits:

- It keeps part as reserves.
- It lends out the rest.
- Those loans often become new deposits elsewhere in the banking system.

That is why the money supply can become much larger than the monetary base.

### Deposit creation formula

If the reserve-deposit ratio is `rr`, then:

```text
Deposits = Reserves / rr
```

This simplified formula works best when:

- banks lend all excess reserves, and
- the public redeposits funds into the banking system instead of holding cash.

### Example

- Deposit = $10,000
- Reserve ratio = 15%
- Reserves kept = $1,500
- Loans made = $8,500

### Money multiplier idea

The money multiplier describes the repeated process:

1. Banks receive deposits.
2. Banks lend part of those deposits.
3. Borrowers spend the loans.
4. The recipients deposit that money into banks.
5. Banks lend again.

### What increases the money supply

- More deposits in banks
- More bank lending
- More reserves supplied by the central bank
- A lower reserve-deposit ratio

### What decreases the money supply

- Bank panics or heavy withdrawals into cash
- A higher reserve-deposit ratio
- Less lending
- Central bank actions that reduce reserves

### Open market operations

- The central bank creates the monetary base.
- It changes reserves mainly through open market operations.
- An **open market purchase** injects reserves into the banking system and tends to increase the money supply.
- An **open market sale** removes reserves and tends to reduce the money supply.

### Important result

If banks were forced to keep 100% reserves and lend nothing, the money supply would contract sharply because deposit creation would stop.

## 6. Quantity Theory of Money

### Core equation

```text
MV = PY
```

Where:

- `M` = money supply
- `V` = velocity of money
- `P` = price level
- `Y` = real output

### What velocity means

- Velocity is the frequency with which money is used to purchase final goods and services.
- It tells us how quickly money circulates through the economy.

### Why the equation is always true

- The quantity equation is an identity.
- It is true because velocity is defined so that the equation holds.

### Long-run quantity theory ideas

In the long run, the theory generally assumes:

- Real GDP is not determined by the growth rate of the money supply.
- Velocity is not determined by the size of the money supply.
- Very large increases in money supply usually lead to very large increases in prices.

### Short run vs. long run

- In the short run, a change in money supply may not translate one-for-one into prices.
- In the long run, persistent rapid money growth is strongly associated with inflation.
- Hyperinflation is usually linked to extremely rapid money creation.

## 7. High-Value Patterns to Remember

- A price increase for one good alone is a relative price change, not necessarily inflation.
- In the base year, CPI = 100.
- Inflation-adjusted values are used to compare purchasing power across time.
- Unexpected inflation helps borrowers and hurts lenders.
- Money has three functions: medium of exchange, unit of account, and store of value.
- Banks create deposits through lending.
- The money supply is usually much larger than the monetary base.
- Open market purchases increase reserves and usually increase the money supply.
- The quantity theory links money growth to inflation in the long run.

## 8. Representative Practice Questions

Use these as quick checks before a quiz or test.

### Inflation

1. If nominal interest is 10% and inflation is 3%, what is the approximate real interest rate?
   Answer: 7%
2. Who benefits from unexpected inflation?
   Answer: Borrowers and others who owe fixed nominal payments
3. Why does high inflation make planning difficult?
   Answer: Because high inflation is often unstable and hard to predict

### CPI

1. What is the CPI in the base year?
   Answer: 100
2. How do you compute inflation from CPI data?
   Answer: Use the percentage change in CPI from one year to the next
3. If you convert a later nominal amount into base-year dollars, does it usually get bigger or smaller when prices have risen over time?
   Answer: Smaller

### Money and Banking

1. What are the three functions of money?
   Answer: Medium of exchange, unit of account, store of value
2. If the reserve ratio is 10%, how much can $1,000 of reserves support in deposits in the simplified model?
   Answer: $10,000
3. What happens to the money supply when the central bank makes an open market purchase?
   Answer: It usually increases

### Quantity Theory

1. What does `MV = PY` mean?
   Answer: Money times velocity equals the price level times real output
2. What is velocity?
   Answer: The speed at which money circulates
3. What typically causes hyperinflation?
   Answer: Extremely rapid growth in the money supply

## 9. Final Review Checklist

Make sure you can:

- Distinguish inflation from a relative price change.
- Compute CPI and inflation rates.
- Convert nominal values into real values.
- Compute approximate and exact real interest rates.
- Explain who gains and loses from unexpected inflation.
- Define money, liquidity, M1, and M2.
- Explain how banks create money through lending.
- Use reserve-deposit ratio formulas.
- Explain how open market operations affect reserves and the money supply.
- State and interpret the quantity equation `MV = PY`.
