// K6 Average-load test for the WooCommerce shop (G01)
// Goal: measure response time and error rate under normal expected load.
// Scenario: a user opens the shop page, searches for a product,
// and opens a product detail page. No order is placed.

import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://157.85.102.236/shop";

// Put 2 or 3 real product URLs here (copy from the browser address bar).
// Use demo products or G01 products, do not touch other groups' data.
const PRODUCT_URLS = [
  "http://157.85.102.236/shop/product/album/",
  "http://157.85.102.236/shop/product/beanie-with-logo/",
];

export const options = {
  stages: [
    { duration: "1m", target: 20 }, // ramp up to 20 VUs
    { duration: "5m", target: 20 }, // stay at 20 VUs (average load)
    { duration: "1m", target: 0 },  // ramp down
  ],
  thresholds: {
    // The project question asks when response time goes above 1 second,
    // so we require 95% of requests to finish under 1000 ms.
    http_req_duration: ["p(95)<1000"],
    // Error rate should stay under 1% in normal load.
    http_req_failed: ["rate<0.01"],
  },
};

export default function () {
  // Step 1: open the shop front page
  let res = http.get(`${BASE_URL}/`);
  check(res, { "home status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1); // think time 1 to 3 seconds

  // Step 2: search for a product
  res = http.get(`${BASE_URL}/?s=shirt&post_type=product`);
  check(res, { "search status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);

  // Step 3: open one product detail page
  const url = PRODUCT_URLS[Math.floor(Math.random() * PRODUCT_URLS.length)];
  res = http.get(url);
  check(res, { "product status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);
}