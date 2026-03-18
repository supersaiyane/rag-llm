import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,          // 10 concurrent users
  duration: "30s",  // test for 30 seconds
};

export default function () {

    const questions = [
        "What does terraform plan do?",
        "How does kubernetes scheduling work?",
        "What is docker networking?",
        "Explain terraform state file",
        "How does kubernetes autoscaling work?"
    ];

    const q = questions[Math.floor(Math.random() * questions.length)];

    const payload = JSON.stringify({
        user_id: "load-test",
        question: q
    });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const res = http.post(
    "http://localhost:8000/chat",
    payload,
    params
  );

  check(res, {
    "status is 200": (r) => r.status === 200,
  });

  sleep(1);
}