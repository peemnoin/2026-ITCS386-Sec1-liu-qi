# SYS-001 Step 10 — targeted manual verification

**Result: PASS — new execution on 18 November 2026, 19:58–20:00 Asia/Bangkok.**

This is a targeted re-execution of Step 10, not a full SYS-001 rerun and not a replacement for the November 11 history.

## Environment and method

- Customer: a new Google Chrome Incognito window, not signed in. Checkout explicitly states “You are currently checking out as a guest.”
- Staff: the existing signed-in Group 01 admin session in a separate ChatGPT in-app browser.
- Existing product: `G01_SYS001_20261111_01 Mug`, THB 199, product page displayed stock 8. Product located through a direct search URL redirect; this is not evidence of using a storefront search control.
- Starting guest cart was empty. Set quantity to 2 and clicked Add to cart, then View cart.
- Clicked Proceed to Checkout. Left contact/billing fields empty. Did not click Place order.
- Clicked the native Chrome toolbar Back button once. Did not reload, navigate directly to Cart, remove/re-add items or use recovery logic between Checkout and the result capture.

## Evidence sequence

| Evidence | Local time | Observation |
|---|---|---|
| [S01 admin before](S01_admin_before.jpg) | 19:58:44 | All orders 129; Processing 36, On hold 4, Completed 62, Cancelled 27; newest visible order #975. |
| [S02 cart before](S02_cart_before.jpg) | 19:59:38 | `/cart/`, Mug quantity 2, line total and estimated total THB 398.00. |
| [S03 checkout](S03_checkout_before_submission.jpg) | 19:59:47 | `/checkout/`, guest session, empty billing/contact fields, Mug quantity 2 and total THB 398.00. |
| Native Back action | 19:59:52 | Clicked browser Back before submitting an order. |
| [S04 cart after Back](S04_cart_after_native_back.jpg) | 20:00:01 | `/cart/`, same Mug quantity 2, line total and estimated total THB 398.00; no reload recovery. |
| [S05 admin after](S05_admin_after.jpg) | 20:00:03 | Reloaded admin Orders: same 129 orders, same status counts and newest visible order #975. |

## Interpretation and limits

The cart-retention and total checks passed. No new submitted order was observed in the admin list; no order-submission action was performed. The before/after list is corroborating UI evidence, not a database audit or proof about hidden draft records/concurrent changes. Do not claim a full server-wide absence of any record mutation.

The only intentional shop mutation was adding two units to the isolated guest cart. No products/coupons were created, no order was submitted, and no stock/order status was edited. The guest window was left on the result cart for inspection. Browser session/cart bookkeeping may persist until expiry. No automated UI/API/load tests were run.

The November 11 Step 10 screenshot remains insufficient to prove that old execution. The **current Step 10 result is PASS from this new dated execution**. SYS-001 Step 4 search, SYS-002 navigation/usage and UI repeatability are outside this run.

`observations.json` contains timestamped accessibility observations and the action note. These are recorded observations, not a video recording.
