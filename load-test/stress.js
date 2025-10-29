import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 },
    { duration: '1m', target: 500 },
    { duration: '1m', target: 1000 },
  ]
};

export default function () {
  const res = http.get('https://quickpizza.grafana.com/');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}