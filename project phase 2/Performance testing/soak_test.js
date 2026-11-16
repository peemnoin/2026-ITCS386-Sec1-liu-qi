// K6 Soak test for the WooCommerce shop (G01)
// Goal: check whether response time or error rate get worse
// when a moderate load runs for a long time (memory leaks,
// resource exhaustion, slow degradation).
// Same user scenario as the other tests. No order is placed.

import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://157.85.102.236/shop";

const PRODUCT_URLS = [
    "http://157.85.102.236/shop/product/album/",
    "http://157.85.102.236/shop/product/beanie-with-logo/",
];

export const options = {
  stages: [
    { duration: "2m", target: 15 },  // ramp up
    { duration: "56m", target: 15 }, // hold for a long time
    { duration: "2m", target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<1000"],
    http_req_failed: ["rate<0.01"],
  },
};

export default function () {
  let res = http.get(`${BASE_URL}/`);
  check(res, { "home status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);

  res = http.get(`${BASE_URL}/?s=shirt&post_type=product`);
  check(res, { "search status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);

  const url = PRODUCT_URLS[Math.floor(Math.random() * PRODUCT_URLS.length)];
  res = http.get(url);
  check(res, { "product status 200": (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);
}