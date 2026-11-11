# ITCS386 Project 2 — System Testing

**Course:** ITCS386 Software Verification and Validation  
**Group:** G01 (Group 01)  
**System under test:** WooCommerce Online Shop (ITCS386 environment)  
**Manual execution date:** 11 November 2026  
**Environment:** [Customer storefront](http://157.85.102.236/shop/) · [Staff admin](http://157.85.102.236/shop/wp-admin/)  
**Test method:** Manual, end-to-end system testing (staff → customer → staff)

> **Scope of this folder:** System Testing only. Automated UI Testing, API Testing and Performance Testing are separate parts of Project 2. The spreadsheet is the source of truth for individual test steps, inputs, expected/actual results and status. This README summarizes what was observed; it does not claim every requirement is fully verified.

## 1. Objective and scope

Verify that the staff-side WooCommerce product, coupon, inventory and order management functions integrate with customer-side product discovery, cart, checkout and order confirmation. The tests cover common purchases as well as invalid coupon and quantity inputs, and an alternative navigation path. All test orders use **Cash on Delivery (COD)**, without real payment.

We designed three cross-role test cases based on the shop features in the WooCommerce Guide (Section 3), and the Project 2 manual system testing rubric:

| Test case | Scenario | Staff → Customer → Staff | Recorded order |
| --- | --- | --- | --- |
| **SYS-001** | Product discovery, purchase & order management | Create G01 product → browse, add two items, COD checkout → verify order and mark completed | **#127**, THB 398 |
| **SYS-002** | Coupon validation & discount | Create G01 product and 10% coupon → reject invalid code, apply/remove discount, COD checkout → inspect order | **#139**, THB 360 |
| **SYS-003** | Inventory limits & guest checkout | Create managed-stock G01 product → reject quantity 0 / over-stock, purchase two items → verify order; account registration conditional | **#142**, THB 300 |

## 2. Deliverables and navigation

```text
System testing/
├── README.md                            # this document
├── test_cases/
│   └── G01_System_Testing_Results_and_RTM.xlsx
└── screenshots/
    ├── SYS-001/                        # Sys001-1.png ... Sys001-15.png
    ├── SYS-002/                        # Sys002-1.png ... Sys002-11.png
    └── SYS-003/                        # Sys003-1.png ... Sys003-13.png
```

The Excel file contains these sheets:

- `START HERE` — environment and execution notes.
- `SYS-001`, `SYS-002`, `SYS-003` — **test case ID, title, objective, preconditions, test data, tester/date, step, side, action, input, expected result, actual result, Pass/Fail and evidence**.
- `RTM` — requirement traceability matrix for the 11 features in the shop guide.
- `SYS-001 REVIEW`, `SYS-002 REVIEW`, `SYS-003 REVIEW` — evidence limitations and follow-up items.
- `DEFECT TEMPLATE` — format for reporting confirmed software defects.
- `UI HANDOFF` — implementation considerations for the Automated UI Testing team.

Screenshots are organized by scenario. **Some screenshots have guest contact details obscured for sharing.** Check every image manually for personal data, credentials or IP addresses before making the repository public. Only the minimum evidence should be published.

## 3. Test cases, data and execution results

### SYS-001 — Product discovery, purchase & order management

**Objective:** Confirm that staff can publish a product, customers can buy it via COD, and staff can locate and update the resulting order.

**Preconditions:** G01 staff access; storefront available; COD active; independent customer browser session.

**Test data:** `G01_SYS001_20261111_01 Mug`; simple product; THB 199; initially 10 in stock; Accessories; purchase quantity 2; subtotal THB 398; guest checkout using fictitious data.

**Observed:** Product was published and visible on the storefront. Cart displayed two units for THB 398. Checkout generated order **#127** for THB 398, and the staff order view confirmed the same product, quantity and total. The status was changed from **Processing** to **Completed**.

**Recorded step statuses in workbook:** 13 PASS; 2 NOT VERIFIED (search interaction and backward-navigation evidence); 1 N/A (guest order history/status in My Account). **These do not imply 16 fully passing steps.**

**Evidence examples:** [published product](screenshots/SYS-001/Sys001-8.png) · [customer product detail](screenshots/SYS-001/Sys001-3.png) · [cart](screenshots/SYS-001/Sys001-9.png). Refer to the workbook's Evidence column for step-level filenames.

### SYS-002 — Coupon validation & discount

**Objective:** Confirm that an invalid coupon is rejected, a valid 10% coupon changes totals correctly, and order records preserve the discount.

**Preconditions:** G01 test product and coupon; working cart and COD checkout.

**Test data actually used:** `G01_SYS002_20261111_Tee`; THB 200 each; quantity 2; subtotal THB 400; a 10%-discount coupon code **`gv82wtw5`**; discount THB 40; total THB 360. This differs from the planned G01-prefixed coupon code.

**Observed:** An invalid coupon code was rejected and the total remained THB 400. Applying the 10% coupon reduced the displayed total to THB 360. Customer confirmation and staff order **#139** both show two units, discount THB 40 and total THB 360; order status **Processing**.

**Recorded review:** 10 PASS; 1 FAIL (test-data naming requirement / procedure, not proof of an application defect); 2 NOT VERIFIED (navigation persistence and coupon usage count). **Important:** The created coupon did not begin with `G01`; this violates the assignment's naming rule and needs a properly prefixed re-run before claiming full procedural compliance.

**Evidence examples:** [invalid coupon](screenshots/SYS-002/Sys002-4.png) · [discounted cart](screenshots/SYS-002/Sys002-7.png) · [staff order](screenshots/SYS-002/Sys002-10.png). Follow the workbook's Evidence column for precise step mapping.

### SYS-003 — Inventory limits, cart changes & guest checkout

**Objective:** Verify stock-aware quantity boundaries and a successful in-stock order; inspect whether guest customer account registration is offered.

**Preconditions:** Staff can publish managed-stock products; COD checkout available; group records isolated.

**Test data:** `G01_SYS003_20261111_StockTest`; THB 150; initially 3 in stock; Accessories; invalid quantities **0** and **4**; valid order quantity **2**.

**Observed:** Browser form validation rejected quantity 0 (minimum 1) and quantity 4 (maximum 3). Two units were added and customer checkout created order **#142** totaling THB 300. The staff order view shows the matching product and quantity with status **Processing**. The public My Account page showed **Login only**, without a visible Register form.

**Recorded step statuses:** 11 PASS; 2 NOT VERIFIED (direct search interaction and post-checkout stock verification); 4 N/A (conditional account-related steps). Initial stock 3 is visible; **stock reduction to 1 has not been evidenced** and should not be reported as verified.

**Evidence examples:** [initial stock](screenshots/SYS-003/Sys003-1.png) · [quantity 0 rejected](screenshots/SYS-003/Sys003-3.png) · [quantity 4 rejected](screenshots/SYS-003/Sys003-4.png) · [order confirmation](screenshots/SYS-003/Sys003-12.png).

## 4. Requirements traceability matrix (RTM)

The full feature-level RTM is in the `RTM` worksheet. `X` means **designed coverage** in a test case; it does **not** automatically mean the requirement passed.

| ID | Feature from WooCommerce Guide §3 | SYS-001 | SYS-002 | SYS-003 | Coverage note |
| --- | --- | :---: | :---: | :---: | --- |
| REQ-01 | Browse catalog, paging and sorting | X | | | Partial — paging not fully evidenced |
| REQ-02 | Search products | X | | X | Planned; search action lacks direct evidence |
| REQ-03 | Categories and category filtering | X | | | Category assigned/visible; filtering should be checked |
| REQ-04 | Product detail, price, stock, images, variations | X | | X | Partial — tested simple products; variable-product flow not tested |
| REQ-05 | Cart add/update/remove and coupons | X | X | X | Core operations represented; review each actual result |
| REQ-06 | Checkout and COD | X | X | X | Three customer orders observed |
| REQ-07 | Customer registration, login, own orders | | | X | Conditional / unavailable for guest registration in observed UI |
| REQ-08 | Product create/edit/delete/stock | X | | X | Partial — creation and stock checked; edit/delete not fully tested |
| REQ-09 | Order list and status management | X | X | X | Order matching and SYS-001 status update |
| REQ-10 | Coupon creation and application | | X | | Observed but coupon naming requirement failed |
| REQ-11 | Customer listing | | | X | Account-related coverage conditional; not fully evidenced |

**Coverage is incomplete for some Guide features.** Before final grading, close gaps with additional steps/evidence inside these scenarios (or add cases if necessary): paging, product variation, staff edit/delete of group-owned records, customer account functions and customer listing. Keep the Excel RTM synchronized with any new tests.

## 5. Deviations, defects and evidence limitations

The observed system did perform the principal product/order/coupon/stock flows. The following items should **not be labeled confirmed application defects** without further reproducible evidence:

| Item | Classification | Required follow-up |
| --- | --- | --- |
| SYS-001 direct search action | NOT VERIFIED | Capture a search query and resulting product listing |
| SYS-001 go-back navigation | NOT VERIFIED | Record checkout → back → cart, showing item persists |
| SYS-001 guest order history | N/A / scope limitation | Guest My Account requires login; compare confirmation order number with staff order instead |
| SYS-002 coupon `gv82wtw5` | TEST PROCEDURE / DATA NONCOMPLIANCE | Create new `G01...` coupon and re-run coupon steps |
| SYS-002 cart navigation / usage count | NOT VERIFIED | Capture navigation persistence and refreshed usage statistics |
| SYS-003 direct search action | NOT VERIFIED | Capture search before opening product details |
| SYS-003 post-checkout stock | NOT VERIFIED | Reopen product/inventory after order #142 and record actual stock |
| SYS-003 account registration | N/A, conditional | Page displays login only; do not alter shared site settings |

**Defect reporting:** For any genuine application failure, create a defect report containing Defect ID, title, preconditions, reproducible steps, expected result, actual result, severity, date and screenshot reference. A template is available in the workbook. No confirmed application defect is asserted solely from the evidence reviewed here.

## 6. Manual execution procedure

1. Log in to the [staff panel](http://157.85.102.236/shop/wp-admin/) using the **G01 normal web login password** (not the API application password).
2. Use separate guest/incognito browser context for [customer storefront](http://157.85.102.236/shop/).
3. Open the selected case in the workbook and follow its actions in order, including invalid inputs and alternative navigation.
4. Create only G01-prefixed products and coupons; never modify demo data or other groups' records.
5. Record actual results and PASS / FAIL / NOT VERIFIED / N/A **per step**, and save screenshots with the filename cited in the Evidence column.
6. For unexpected behavior, distinguish application defect from test-environment, missing evidence or test-procedure error; add a defect report only if confirmed.
7. Update the RTM after adding or changing test coverage.

**Re-execution:** Use unique run IDs for newly created records (e.g., `G01_SYS001_20261120_1430_Mug`). Avoid relying on mutable shared data. Since orders are persistent, do not recreate them merely to repeat a screenshot without documenting the run.

## 7. Security and responsible use

- The shop is on a **shared classroom server** and uses plain HTTP. Never commit group credentials, application passwords, authentication cookies, request headers containing secrets or real personal information.
- The `ITCS386_Group_Accounts.xlsx` file is **not part of this repository** and must not be uploaded.
- Use fictional email addresses, names, phone numbers and shipping details in future runs.
- Screenshots in the supplied package have selected sensitive areas obscured. **Manually inspect all images before publishing**, including any new screenshots.
- Do not edit/delete another group's products, coupons, orders or customers.

## 8. Automated UI Testing handoff

The UI team should automate the **same three scenarios and expected outcomes**, not invent different scenarios. The workbook's `UI HANDOFF` worksheet provides further implementation notes. Use Selenium WebDriver, Robot Framework or Cypress, assert visible page content and computed totals, use explicit waits and unique G01-prefixed test records on repeat runs. Keep UI test scripts and full-run screenshots in the separate `UI testing/` directory.

## 9. Sources and assignment alignment

- ITCS386 Project 2 Descriptions v5 — System Testing requirements, test case template, screenshots, RTM and GitHub submission rules.
- WooCommerce Shop API Guide — ITCS386 environment, shop features, staff/customer roles and COD checkout.
- G01 manual screenshots and test-case workbook, dated 11 November 2026.

**Deadline:** 25 November 2026, 17:00 (repository must be pushed before the cutoff). Progress presentation: 19 November 2026. 
