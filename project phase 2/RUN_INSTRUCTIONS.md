# ITCS386 Project 2 — Step-by-Step Run Instructions (Windows PowerShell)

This guide explains how to set up and run every part of **Group 01's Project 2** on **Windows PowerShell**.

---

## 1. API Testing (`project phase 2/API testing/`)

### 1.1 Required Software & Setup
- **Python 3.12+** (`python --version`)
- **Packages:** `pytest`, `requests`, `python-dotenv` (listed in `API testing/requirements.txt`)

Open PowerShell and navigate to `API testing`:

```powershell
cd "project phase 2\API testing"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 1.2 Credentials Configuration
Create a new file named `.env` in the `API testing` folder and add these two lines. Replace the values with Group 01's API username and **Application Password** (from the private group account sheet):
```text
WC_API_USERNAME=your_g01_api_username
WC_API_PASSWORD=your_g01_application_password
```
   > **Security:** Never commit `.env` to Git (it is ignored by `.gitignore`).

### 1.3 Running the Tests
- **Quick connectivity smoke check (no auth required):**
  ```powershell
  python check_api.py
  ```
- **Run one test suite:**
  ```powershell
  python -m pytest tests/test_create_product.py -v
  python -m pytest tests/test_update_product.py -v
  python -m pytest tests/test_add_to_cart.py -v
  ```
- **Run all 31 API tests with one command (and save output):**
  ```powershell
  python -m pytest tests -v | Tee-Object -FilePath api_run_log.txt
  ```

### 1.4 Expected Output & Results
- **Expected:** `27 passed, 4 failed` (`CP04`, `CP06`, `UP05`, `UP07` fail because the WooCommerce API accepts negative prices and silently clears/drops non-numeric prices instead of returning HTTP 400).
- **Saved Evidence:** `API_TEST_RESULTS.md`, `api_test_execution.png`, `test_execution.png`.
- **Troubleshooting:**
  - `ModuleNotFoundError: No module named 'dotenv'`: Activate `.venv` (`.\.venv\Scripts\Activate.ps1`) and run `pip install -r requirements.txt`.
  - `Missing WC_API_USERNAME or WC_API_PASSWORD`: Verify `.env` exists in `API testing/` (not only in the repo root).
  - `401 Unauthorized`: Ensure you used the **Application Password**, not the normal WordPress web login password.

---

## 2. System Testing (`project phase 2/System testing/`)

Manual system tests are **not executed via a script**. They are performed by hand in a browser and recorded in `System testing/test_cases/G01_System_Testing_Results_and_RTM.xlsx`.

### 2.1 How to Execute Manually
1. Open `G01_System_Testing_Results_and_RTM.xlsx` and read sheets `SYS-001`, `SYS-002`, and `SYS-003`.
2. Open **two separate browser windows** (e.g., normal Chrome for **Staff** at `http://157.85.102.236/shop/wp-admin/` using the normal web password, and an **Incognito/Private** window for **Guest Customer** at `http://157.85.102.236/shop/`).
3. Follow each step in order. Use a unique `G01_SYS00x_<YYYYMMDD>_...` prefix for every product and coupon you create. Use fictional customer names, emails (`@example.com`), addresses, and phone numbers.
4. Capture a screenshot for each step and save it under `System testing/screenshots/SYS-001/`, `SYS-002/`, or `SYS-003/` (redact any sensitive info or IPs before pushing).
5. Record the **Actual Result** honestly per step:
   - `PASS`: Observed UI matches Expected Result and has supporting screenshot.
   - `FAIL`: Behavior or rule failed (e.g., `SYS-002` Step 2 coupon missing `G01` prefix, or an application defect logged in `DEFECT TEMPLATE`).
   - `NOT VERIFIED`: Step was not captured or screenshot does not prove the claim.
   - `N/A`: Conditional step cannot run due to site configuration (e.g., registration disabled).
6. Update the `RTM` sheet whenever coverage changes so `COVERED` / `PARTIAL` / `CONDITIONAL` reflects actual verified evidence.

---

## 3. Automated UI Testing (`project phase 2/UI testing/`)

### 3.1 Setup & Dependencies
- **Requirements:** Python 3.12+, Google Chrome installed, `selenium`, `pytest`, `python-dotenv` (`UI testing/requirements.txt`). Selenium 4.52.0 uses Selenium Manager to download ChromeDriver automatically.

```powershell
cd "project phase 2\UI testing"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a new file named `.env` in the `UI testing` folder and add these two lines. Replace the values with Group 01's **normal Staff web login**:
```text
SHOP_ADMIN_USERNAME=your_g01_staff_username
SHOP_ADMIN_PASSWORD=your_g01_staff_password
```

### 3.2 Running the Tests
- **Run individual tests:**
  ```powershell
  pytest test_ui_001.py -v -s
  pytest test_ui_002.py -v -s
  pytest test_ui_003.py -v -s
  ```
- **Run all three UI tests together:**
  ```powershell
  pytest test_ui_001.py test_ui_002.py test_ui_003.py -v -s
  ```
  > Note: Avoid running bare `pytest` without filenames, because `test_browser.py` is an older scratch smoke-test file.
- **Verify repeatability (run twice):**
  ```powershell
  pytest test_ui_001.py test_ui_002.py test_ui_003.py -v -s
  pytest test_ui_001.py test_ui_002.py test_ui_003.py -v -s
  ```
  Each run uses `datetime.now().strftime("%Y%m%d_%H%M%S")` to create unique products, coupons, and guest emails so the second run does not collide with the first.

### 3.3 Evidence & Troubleshooting
- Save terminal screenshots and screen recordings under `UI testing/evidence/ui001/`, `ui002/`, `ui003/` (or link large `.mp4` recordings in `UI testing/README.md`).
- **Troubleshooting:**
  - `TimeoutException`: The shared classroom server can be slow; re-run or check internet connectivity to `157.85.102.236`.
  - `SHOP_ADMIN_USERNAME is missing`: Ensure `.env` is in `UI testing/` and `.venv` is active.

---

## 4. Performance Testing (`project phase 2/Performance testing/`)

### 4.1 K6 Installation (Windows)
Install K6 via `winget` or `choco` in PowerShell, then reopen PowerShell:
```powershell
winget install k6 --source winget
k6 version
```

### 4.2 Safety Precautions
- **Do NOT add `POST` order/checkout calls** to K6 scripts; orders persist on the shared server.
- **Do NOT run `stress_test.js`, `spike_test.js`, or `soak_test.js` (60 min) against the shared server without lecturer/team authorization**, especially right before deadlines when other groups are testing.

### 4.3 Commands for Each Test Type
From `project phase 2\Performance testing\`:

```powershell
New-Item -ItemType Directory -Force results | Out-Null
$ts = Get-Date -Format "yyyyMMdd_HHmm"

# 1. Average-load (7 min)
k6 run avg_load_test.js --summary-export "results/avg_load_$ts.json" | Tee-Object -FilePath "results/avg_load_$ts.txt"

# 2. Stress (11 min)
k6 run stress_test.js --out csv="results/stress_$ts.csv" --summary-export "results/stress_$ts.json" | Tee-Object -FilePath "results/stress_$ts.txt"

# 3. Spike (~7.5 min)
k6 run spike_test.js --out csv="results/spike_$ts.csv" --summary-export "results/spike_$ts.json" | Tee-Object -FilePath "results/spike_$ts.txt"

# 4. Soak (60 min)
k6 run soak_test.js --out csv="results/soak_$ts.csv" --summary-export "results/soak_$ts.json" | Tee-Object -FilePath "results/soak_$ts.txt"

# Short live-demo run for presentation (45 sec, 10 VUs)
k6 run --stage 15s:10 --stage 30s:10 avg_load_test.js
```

### 4.4 Interpreting Output
- `http_req_duration` `p(95)`: 95% of requests completed faster than this time (threshold: `< 1000 ms`).
- `http_req_failed`: Percentage of failed HTTP requests / timeouts (threshold: `< 1%` normal/soak, `< 5%` stress/spike).
- `vus_max`: Maximum concurrent virtual users reached during the run.
- Note: K6 exiting with non-zero code when `thresholds on metrics 'http_req_duration' have been crossed` means the **server** exceeded 1 s, not that the script crashed.

