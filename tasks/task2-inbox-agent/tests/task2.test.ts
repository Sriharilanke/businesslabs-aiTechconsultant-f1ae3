import { runTask2Evaluations } from "../src/evaluation/run_evals";

async function main() {
  console.log("Running Task 2 Test Suite...");
  const report = await runTask2Evaluations();
  if (report.accuracy < 90) {
    console.error(`Task 2 Test Suite Failed with accuracy: ${report.accuracy}%`);
    process.exit(1);
  }
  console.log(`Task 2 Test Suite Passed with ${report.passed}/${report.total} tests passing (${report.accuracy}%)!`);
  process.exit(0);
}

main().catch(err => {
  console.error("Test execution error:", err);
  process.exit(1);
});
