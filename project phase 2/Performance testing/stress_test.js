// K6 Stress test for the WooCommerce shop (G01)
// Goal: find the point where the system starts to show problems
// (response time above 1 second or errors) by increasing VUs in steps.
// Same user scenario as the average-load test. No order is placed.

import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://157.85.102.236/shop";

const PRODUCT_URLS = [
    "http://157.85.102.236/shop/product/album/",
    "http://157.85.102.236/shop/product/beanie-with-logo/",
];

export const options = {
  stages: [
    { duration: "2m", target: 20 },  // normal load
    { duration: "2m", target: 40 },
    { duration: "2m", target: 60 },
    { duration: "2m", target: 80 },
    { duration: "2m", target: 100 }, // beyond expected load
    { duration: "1m", target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<1000"],
    http_req_failed: ["rate<0.05"],

  },
};

export default function () {
  let res = http.get(`${BASE_URL}/`);
  check(res, { "home status 200": (r) => r.status === 200 });
  sleep(Math.random() + 0.5);

  res = http.get(`${BASE_URL}/?s=shirt&post_type=product`);
  check(res, { "search status 200": (r) => r.status === 200 });
  sleep(Math.random() + 0.5);

  const url = PRODUCT_URLS[Math.floor(Math.random() * PRODUCT_URLS.length)];
  res = http.get(url);
  check(res, { "product status 200": (r) => r.status === 200 });
  sleep(Math.random() + 0.5);
}