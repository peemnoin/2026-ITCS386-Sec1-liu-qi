// K6 Spike test for the WooCommerce shop (G01)
// Goal: see how the system behaves when traffic suddenly jumps,
// and how long it takes to return to normal service after the spike.
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
    { duration: "1m", target: 5 },   // normal quiet traffic (baseline)
    { duration: "10s", target: 50 }, // sudden spike
    { duration: "1m", target: 50 },  // hold the spike
    { duration: "10s", target: 5 },  // spike ends (at 140 s)
    { duration: "5m", target: 5 },   // watch the recovery
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
